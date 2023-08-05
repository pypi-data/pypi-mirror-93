"""Custom package sources used for feeding checks."""

import os
from collections import defaultdict, deque
from collections.abc import Set
from dataclasses import dataclass
from operator import attrgetter

from pkgcore.ebuild.repository import UnconfiguredTree
from pkgcore.restrictions import packages
from snakeoil.osutils import listdir_files, pjoin

from . import addons, base
from .eclass import Eclass, EclassAddon
from .packages import FilteredPkg, RawCPV, WrappedPkg
from .profiles import ProfileAddon, ProfileNode


class Source:
    """Base template for a source."""

    scope = base.repo_scope
    required_addons = ()

    def __init__(self, options, source):
        self.options = options
        self.source = source

    def __iter__(self):
        yield from self.source

    def itermatch(self, restrict, **kwargs):
        yield from self.source


class EmptySource(Source):
    """Empty source meant for skipping item feed."""

    def __init__(self, scope, options):
        super().__init__(options, source=())
        self.scope = scope


class RepoSource(Source):
    """Base template for a repository source."""

    scope = base.version_scope

    def __init__(self, options, source=None):
        self.options = options
        self.repo = options.target_repo
        self._source = source

    @property
    def source(self):
        """Source that packages are pulled from."""
        if self._source is not None:
            return self._source
        return self.repo

    def itermatch(self, restrict, sorter=sorted, **kwargs):
        """Yield packages matching the given restriction from the selected source."""
        return self.source.itermatch(restrict, sorter=sorter, **kwargs)


class LatestVersionsFilter:
    """Filter source packages, yielding those from the latest non-VCS and VCS slots."""

    def __init__(self, source_iter):
        self._source_iter = source_iter
        self._pkg_cache = deque()
        self._pkg_marker = None

    def __iter__(self):
        return self

    def __next__(self):
        # refill pkg cache
        if not self._pkg_cache:
            if self._pkg_marker is None:
                self._pkg_marker = next(self._source_iter)
            pkg = self._pkg_marker
            key = pkg.key
            selected_pkgs = {}
            pkgs = []

            # determine the latest non-VCS and VCS pkgs for each slot
            while key == pkg.key:
                if pkg.live:
                    selected_pkgs[f'vcs-{pkg.slot}'] = pkg
                else:
                    selected_pkgs[pkg.slot] = pkg

                pkgs.append(pkg)

                try:
                    pkg = next(self._source_iter)
                except StopIteration:
                    self._pkg_marker = None
                    break

            if self._pkg_marker is not None:
                self._pkg_marker = pkg

            selected_pkgs = set(selected_pkgs.values())
            self._pkg_cache.extend(
                FilteredPkg(pkg=pkg) if pkg not in selected_pkgs else pkg for pkg in pkgs)

        return self._pkg_cache.popleft()


class LatestPkgsFilter:
    """Flag the latest non-VCS and VCS slots for filtering package sets."""

    def __init__(self, source_iter):
        self._source_iter = source_iter

    def __iter__(self):
        return self

    def __next__(self):
        pkgs = next(self._source_iter)
        selected_pkgs = {}

        # determine the latest non-VCS and VCS pkgs for each slot
        for pkg in pkgs:
            if pkg.live:
                selected_pkgs[f'vcs-{pkg.slot}'] = pkg
            else:
                selected_pkgs[pkg.slot] = pkg

        selected_pkgs = set(selected_pkgs.values())
        return [FilteredPkg(pkg=pkg) if pkg not in selected_pkgs else pkg for pkg in pkgs]


class FilteredRepoSource(RepoSource):
    """Ebuild repository source supporting custom package filtering."""

    def __init__(self, pkg_filter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pkg_filter = pkg_filter

    def itermatch(self, restrict, **kwargs):
        yield from self._pkg_filter(super().itermatch(restrict, **kwargs))


class FilteredPackageRepoSource(FilteredRepoSource):
    """Ebuild repository source supporting custom package filtering."""

    scope = base.package_scope


class EclassRepoSource(RepoSource):
    """Repository eclass source."""

    scope = base.eclass_scope
    required_addons = (EclassAddon,)

    def __init__(self, *args, eclass_addon, **kwargs):
        super().__init__(*args, **kwargs)
        self.eclasses = eclass_addon._eclass_repos[self.repo.location]
        self.eclass_dir = pjoin(self.repo.location, 'eclass')

    def itermatch(self, restrict, **kwargs):
        if isinstance(restrict, Set):
            # --commits or path restriction
            eclasses = sorted(restrict.intersection(self.eclasses))
        else:
            # matching all eclasses
            eclasses = self.eclasses

        for name in eclasses:
            yield Eclass(name, pjoin(self.eclass_dir, f'{name}.eclass'))


@dataclass
class Profile:
    """Generic profile object."""
    node: ProfileNode
    files: set


class ProfilesRepoSource(RepoSource):
    """Repository profiles file source."""

    scope = base.profile_node_scope

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profiles_dir = self.repo.config.profiles_base
        self.non_profile_dirs = {
            f'profiles/{x}' for x in ProfileAddon.non_profile_dirs}
        self._prefix_len = len(self.repo.location.rstrip(os.sep)) + 1

    def itermatch(self, restrict, **kwargs):
        if isinstance(restrict, Set):
            # --commits or path restriction
            paths = defaultdict(list)
            for x in restrict:
                paths[pjoin(self.repo.location, os.path.dirname(x))].append(os.path.basename(x))
            for root, files in sorted(paths.items()):
                yield Profile(ProfileNode(root), set(files))
        else:
            # matching all profiles
            for root, _dirs, files in os.walk(self.profiles_dir):
                if root[self._prefix_len:] not in self.non_profile_dirs:
                    yield Profile(ProfileNode(root), set(files))


class _RawRepo(UnconfiguredTree):
    """Repository that allows matching against mismatched/invalid package names."""

    def __init__(self, repo):
        super().__init__(repo.location)

    def _get_versions(self, catpkg):
        """Pass through all packages that end with ".ebuild" extension.

        Deviates from parent in that no package name check is done.
        """
        cppath = pjoin(self.base, catpkg[0], catpkg[1])
        pkg = f'{catpkg[-1]}-'
        lp = len(pkg)
        extension = self.extension
        ext_len = -len(extension)
        try:
            return tuple(
                x[lp:ext_len] for x in listdir_files(cppath)
                if x[ext_len:] == extension)
        except EnvironmentError as e:
            path = pjoin(self.base, os.sep.join(catpkg))
            raise KeyError(f'failed fetching versions for package {path}: {e}') from e


class RawRepoSource(RepoSource):
    """Ebuild repository source returning raw CPV objects."""

    def itermatch(self, restrict, **kwargs):
        self.repo = _RawRepo(self.repo)
        yield from super().itermatch(restrict, raw_pkg_cls=RawCPV, **kwargs)


class RestrictionRepoSource(RepoSource):
    """Ebuild repository source supporting custom restrictions."""

    def __init__(self, restriction, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.restriction = restriction

    def itermatch(self, restrict, **kwargs):
        restrict = packages.AndRestriction(*(restrict, self.restriction))
        yield from super().itermatch(restrict, **kwargs)


class UnmaskedRepoSource(RepoSource):
    """Repository source that uses profiles/package.mask to filter packages."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._filtered_repo = self.options.domain.filter_repo(
            self.repo, pkg_masks=(), pkg_unmasks=(), pkg_filters=(),
            pkg_accept_keywords=(), pkg_keywords=(), profile=False)

    def itermatch(self, restrict, **kwargs):
        yield from self._filtered_repo.itermatch(restrict, **kwargs)


class _SourcePkg(WrappedPkg):
    """Package object with file contents injected as an attribute."""

    __slots__ = ('lines',)

    def __init__(self, pkg):
        super().__init__(pkg)
        self.lines = tuple(pkg.ebuild.text_fileobj())


class EbuildFileRepoSource(RepoSource):
    """Ebuild repository source yielding package objects and their file contents."""

    def itermatch(self, restrict, **kwargs):
        for pkg in super().itermatch(restrict, **kwargs):
            yield _SourcePkg(pkg)


class _ParsedPkg(WrappedPkg):
    """Package object with parse tree and raw bytes data injected as attributes."""

    __slots__ = ('data', 'tree')

    def __init__(self, pkg, data, tree):
        super().__init__(pkg)
        self.data = data
        self.tree = tree

    def node_str(self, node):
        """Return the ebuild string associated with a given parse tree node."""
        return self.data[node.start_byte:node.end_byte].decode('utf8')


class EbuildParseRepoSource(RepoSource):
    """Ebuild repository source yielding package objects and their file contents."""

    required_addons = (addons.BashAddon,)

    def __init__(self, *args, bash_addon, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = bash_addon.parser

    def itermatch(self, restrict, **kwargs):
        for pkg in super().itermatch(restrict, **kwargs):
            data = pkg.ebuild.bytes_fileobj().read()
            tree = self.parser.parse(data)
            yield _ParsedPkg(pkg, data, tree)


class _CombinedSource(RepoSource):
    """Generic source combining packages into similar chunks."""

    def keyfunc(self, pkg):
        """Function targeting attribute used to group packages."""
        raise NotImplementedError(self.keyfunc)

    def itermatch(self, restrict, **kwargs):
        key = None
        chunk = None
        for pkg in super().itermatch(restrict, **kwargs):
            new = self.keyfunc(pkg)
            if new == key:
                chunk.append(pkg)
            else:
                if chunk is not None:
                    yield chunk
                chunk = [pkg]
                key = new
        if chunk is not None:
            yield chunk


class PackageRepoSource(_CombinedSource):
    """Ebuild repository source yielding lists of versioned packages per package."""

    scope = base.package_scope
    keyfunc = attrgetter('key')


class CategoryRepoSource(_CombinedSource):
    """Ebuild repository source yielding lists of versioned packages per category."""

    scope = base.category_scope
    keyfunc = attrgetter('category')


class RepositoryRepoSource(RepoSource):
    """Ebuild repository source yielding lists of versioned packages per package."""

    scope = base.repo_scope


class _FilteredSource(RawRepoSource):
    """Generic source yielding selected attribute from matching packages."""

    def keyfunc(self, pkg):
        raise NotImplementedError(self.keyfunc)

    def itermatch(self, restrict, **kwargs):
        key = None
        for pkg in super().itermatch(restrict, **kwargs):
            new = self.keyfunc(pkg)
            if new != key:
                if key is not None:
                    yield key
                key = new
        if key is not None:
            yield key


class UnversionedSource(_FilteredSource):
    """Source yielding unversioned atoms from matching packages."""

    keyfunc = attrgetter('unversioned_atom')


class VersionedSource(_FilteredSource):
    """Source yielding versioned atoms from matching packages."""

    keyfunc = attrgetter('versioned_atom')


def init_source(source, options, addons_map=None):
    """Initialize a given source."""
    if isinstance(source, tuple):
        if len(source) == 3:
            cls, args, kwargs = source
            kwargs = dict(kwargs)
            # initialize wrapped source
            if 'source' in kwargs:
                kwargs['source'] = init_source(kwargs['source'], options, addons_map)
        else:
            cls, args = source
            kwargs = {}
    else:
        cls = source
        args = ()
        kwargs = {}
    for addon in cls.required_addons:
        kwargs[base.param_name(addon)] = addons.init_addon(addon, options, addons_map)
    return cls(*args, options, **kwargs)
