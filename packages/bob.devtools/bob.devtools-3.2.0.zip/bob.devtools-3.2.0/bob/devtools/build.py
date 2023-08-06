#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tools for self-building and other utilities."""


import os
import re
import sys
import json
import glob
import copy
import logging
import platform
import subprocess
import contextlib
import distutils.version

import yaml
import conda_build.api

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def root_logger_protection():
    """Protects the root logger against spurious (conda) manipulation"""

    root_logger = logging.getLogger()
    level = root_logger.level
    handlers = copy.copy(root_logger.handlers)

    yield

    root_logger.setLevel(level)
    root_logger.handlers = handlers


def comment_cleanup(lines):
    """Cleans-up comments and empty lines from textual data read from files."""

    no_comments = [k.partition("#")[0].strip() for k in lines]
    return [k for k in no_comments if k]


def load_order_file(path):
    """Loads an order.txt style file, removes empty lines and comments."""

    with open(path, "rt") as f:
        return comment_cleanup(f.readlines())


def conda_arch():
    """Returns the current OS name and architecture as recognized by conda."""

    r = "unknown"
    if platform.system().lower() == "linux":
        r = "linux"
    elif platform.system().lower() == "darwin":
        r = "osx"
    else:
        raise RuntimeError('Unsupported system "%s"' % platform.system())

    if platform.machine().lower() == "x86_64":
        r += "-64"
    elif platform.machine().lower() == "aarch64":
        r += "-aarch64"
    else:
        raise RuntimeError('Unsupported machine type "%s"' % platform.machine())

    return r


def should_skip_build(metadata_tuples):
    """Takes the output of render_recipe as input and evaluates if this
    recipe's build should be skipped."""

    return all(m[0].skip() for m in metadata_tuples)


def next_build_number(channel_url, basename):
    """Calculates the next build number of a package given the channel.

    This function returns the next build number (integer) for a package given
    its resulting tarball base filename (can be obtained with
    :py:func:`get_output_path`).


    Args:

      channel_url: The URL where to look for packages clashes (normally a beta
        channel)
      basename: The tarball basename to check on the channel

    Returns: The next build number with the current configuration.  Zero (0) is
    returned if no match is found.  Also returns the URLs of the packages it
    finds with matches on the name, version and python-version, ordered by
    (reversed) build-number.
    """

    from conda.exports import fetch_index
    from conda.core.index import calculate_channel_urls

    # get the channel index
    channel_urls = calculate_channel_urls(
        [channel_url], prepend=False, use_local=False
    )
    logger.debug("Downloading channel index from %s", channel_urls)
    index = fetch_index(channel_urls=channel_urls)

    # remove .tar.bz2/.conda from name, then split from the end twice, on '-'
    if basename.endswith(".tar.bz2"):
        name, version, build = basename[:-8].rsplit("-", 2)
    elif basename.endswith(".conda"):
        name, version, build = basename[:-6].rsplit("-", 2)
    else:
        raise RuntimeError(
            "Package name %s does not end in either "
            ".tar.bz2 or .conda" % (basename,)
        )

    # remove the build number as we're looking for the next value
    # examples to be coped with:
    # vlfeat-0.9.20-0 -> '0'
    # vlfeat-0.9.21-h18fa195_0 -> 'h18fa195_0'
    # tqdm-4.11.1-py36_0 -> 'py36_0'
    # websocket-client-0.47.0-py27haf68d3b_0 -> 'py27haf68d3b_0'
    # websocket-client-0.47.0-py36haf68d3b_0 -> 'py36haf68d3b_0'
    build_variant = build.rsplit("_", 1)[0]
    # vlfeat-0.9.20-0 -> '0'
    # vlfeat-0.9.21-h18fa195_0 -> 'h18fa195'
    # tqdm-4.11.1-py36_0 -> 'py36'
    # websocket-client-0.47.0-py27haf68d3b_0 -> 'py27haf68d3b'
    # websocket-client-0.47.0-py36haf68d3b_0 -> 'py36haf68d3b'
    build_variant = build_variant.split("h", 1)[0]
    # vlfeat-0.9.20-0 -> '0'
    # vlfeat-0.9.21-h18fa195_0 -> ''
    # tqdm-4.11.1-py36_0 -> 'py36'
    # websocket-client-0.47.0-py27haf68d3b_0 -> 'py27'
    # websocket-client-0.47.0-py36haf68d3b_0 -> 'py36'
    if re.match("^[0-9]+$", build_variant) is not None:
        build_variant = ""

    # search if package with the same characteristics
    urls = {}
    build_number = 0
    for dist in index:
        if (
            dist.name == name
            and dist.version == version
            and dist.build_string.startswith(build_variant)
        ):  # match!
            url = index[dist].url
            logger.debug(
                "Found match at %s for %s-%s-%s",
                url,
                name,
                version,
                build_variant,
            )
            build_number = max(build_number, dist.build_number + 1)
            urls[index[dist].timestamp] = url.replace(channel_url, "")

    sorted_urls = [urls[k] for k in reversed(list(urls.keys()))]

    return build_number, sorted_urls


def make_conda_config(config, python, append_file, condarc_options):
    """Creates a conda configuration for a build merging various sources.

    This function will use the conda-build API to construct a configuration by
    merging different sources of information.

    Args:

      config: Path leading to the ``conda_build_config.yaml`` to use
      python: The version of python to use for the build as ``x.y`` (e.g.
        ``3.6``)
      append_file: Path leading to the ``recipe_append.yaml`` file to use
      condarc_options: A dictionary (typically read from a condarc YAML file)
        that contains build and channel options

    Returns: A dictionary containing the merged configuration, as produced by
    conda-build API's ``get_or_merge_config()`` function.
    """

    with root_logger_protection():
        from conda_build.conda_interface import url_path

        retval = conda_build.api.get_or_merge_config(
            None,
            variant_config_files=config,
            python=python,
            append_sections_file=append_file,
            **condarc_options,
        )

    retval.channel_urls = []

    for url in condarc_options["channels"]:
        # allow people to specify relative or absolute paths to local channels
        #    These channels still must follow conda rules - they must have the
        #    appropriate platform-specific subdir (e.g. win-64)
        if os.path.isdir(url):
            if not os.path.isabs(url):
                url = os.path.normpath(
                    os.path.abspath(os.path.join(os.getcwd(), url))
                )
            with root_logger_protection():
                url = url_path(url)
        retval.channel_urls.append(url)

    return retval


def get_output_path(metadata, config):
    """Renders the recipe and returns the name of the output file."""

    with root_logger_protection():
        return conda_build.api.get_output_file_paths(metadata, config=config)


def get_rendered_metadata(recipe_dir, config):
    """Renders the recipe and returns the interpreted YAML file."""

    with root_logger_protection():
        return conda_build.api.render(recipe_dir, config=config)


def get_parsed_recipe(metadata):
    """Renders the recipe and returns the interpreted YAML file."""

    with root_logger_protection():
        output = conda_build.api.output_yaml(metadata[0][0])
    return yaml.load(output, Loader=yaml.FullLoader)


def exists_on_channel(channel_url, basename):
    """Checks on the given channel if a package with the specs exist.

    This procedure always ignores the package hash code, if one is set.  It
    differentiates between `.conda` and `.tar.bz2` packages.

    Args:

      channel_url: The URL where to look for packages clashes (normally a beta
        channel)
      basename: The basename of the tarball to search for

    Returns: A complete package url, if the package already exists in the
    channel or ``None`` otherwise.
    """

    build_number, urls = next_build_number(channel_url, basename)

    def _get_build_number(name):

        # remove .tar.bz2/.conda from name, then split from the end twice, on
        # '-'
        if name.endswith(".conda"):
            name, version, build = name[:-6].rsplit("-", 2)
        elif name.endswith(".tar.bz2"):
            name, version, build = name[:-8].rsplit("-", 2)
        else:
            raise RuntimeError(
                "Package name %s does not end in either "
                ".tar.bz2 or .conda" % (name,)
            )

        # remove the build number as we're looking for the next value
        # examples to be coped with:
        # vlfeat-0.9.20-0 -> '0'
        # vlfeat-0.9.21-h18fa195_0 -> 'h18fa195_0'
        # tqdm-4.11.1-py36_0 -> 'py36_0'
        # untokenize-0.1.1-py_0.conda -> 'py_0'
        # websocket-client-0.47.0-py27haf68d3b_0 -> 'py27haf68d3b_0'
        # websocket-client-0.47.0-py36haf68d3b_0 -> 'py36haf68d3b_0'
        s = build.rsplit("_", 1)
        return s[1] if len(s) == 2 else s[0]

    self_build_number = _get_build_number(basename)
    other_build_numbers = dict(
        [(k, _get_build_number(os.path.basename(k))) for k in urls]
    )

    if self_build_number in other_build_numbers.values():
        pkg_type = ".conda" if basename.endswith(".conda") else ".tar.bz2"
        for k, v in other_build_numbers.items():
            if k.endswith(pkg_type):  # match
                return "".join((channel_url, k))


def remove_pins(deps):
    return [ll.split()[0] for ll in deps]


def parse_dependencies(recipe_dir, config):

    metadata = get_rendered_metadata(recipe_dir, config)
    recipe = get_parsed_recipe(metadata)
    build_requirements = remove_pins(recipe["requirements"].get("build", []))
    # causes conflicts on macOS
    if "llvm-tools" in build_requirements:
        build_requirements.remove("llvm-tools")
    return (
        build_requirements
        + remove_pins(recipe["requirements"].get("host", []))
        + recipe["requirements"].get("run", [])
        + recipe.get("test", {}).get("requires", [])
        + ["pip"]  # required for installing further packages
        + ["bob.buildout"]  # required for basic bootstrap of most recipes
        + ["ipython"]  # for ipdb
        # Also add anaconda compilers to make sure source installed packages are
        # compiled properly
        + [
            "clangxx_osx-64"
            if platform.system() == "Darwin"
            else "gxx_linux-64"
        ]
    )
    # by last, packages required for local dev


def get_env_directory(conda, name):
    """Get the directory of a particular conda environment or fail silently."""

    cmd = [conda, "env", "list", "--json"]
    output = subprocess.check_output(cmd)
    data = json.loads(output)
    paths = data.get("envs", [])

    if not paths:
        # real error condition, reports it at least, but no exception raising...
        logger.error("No environments in conda (%s) installation?", conda)
        return None

    if name in ("base", "root"):
        return paths[0]  # first environment is base

    # else, must search for the path ending in ``/name``
    retval = [k for k in paths if k.endswith(os.sep + name)]
    if retval:
        return retval[0]

    # if no environment with said name is found, return ``None``
    return None


def conda_create(conda, name, overwrite, condarc, packages, dry_run, use_local):
    """Creates a new conda environment following package specifications.

    This command can create a new conda environment following the list of input
    packages.  It will overwrite an existing environment if indicated.

    Args:
      conda: path to the main conda executable of the installation
      name: the name of the environment to create or overwrite
      overwrite: if set to ```True``, overwrite potentially existing environments
        with the same name
      condarc: a dictionary of options for conda, including channel urls
      packages: the package list specification
      dry_run: if set, then don't execute anything, just print stuff
      use_local: include the local conda-bld directory as a possible installation
        channel (useful for testing multiple interdependent recipes that are
        built locally)
    """

    from .bootstrap import run_cmdline

    specs = []
    for k in packages:
        k = " ".join(k.split()[:2])  # remove eventual build string
        if any(elem in k for elem in "><|"):
            specs.append(k.replace(" ", ""))
        else:
            specs.append(k.replace(" ", "="))

    # if the current environment exists, delete it first
    envdir = get_env_directory(conda, name)
    if envdir is not None:
        if overwrite:
            cmd = [conda, "env", "remove", "--yes", "--name", name]
            logger.debug("$ " + " ".join(cmd))
            if not dry_run:
                run_cmdline(cmd)
        else:
            raise RuntimeError(
                "environment `%s' exists in `%s' - use "
                "--overwrite to overwrite" % (name, envdir)
            )

    cmdline_channels = ["--channel=%s" % k for k in condarc["channels"]]
    cmd = [
        conda,
        "create",
        "--yes",
        "--name",
        name,
        "--override-channels",
    ] + cmdline_channels
    if dry_run:
        cmd.append("--dry-run")
    if use_local:
        cmd.append("--use-local")
    cmd.extend(sorted(specs))
    run_cmdline(cmd)

    # creates a .condarc file to sediment the just created environment
    if not dry_run:
        # get envdir again - it may just be created!
        envdir = get_env_directory(conda, name)
        destrc = os.path.join(envdir, "condarc")
        logger.info("Creating %s...", destrc)
        with open(destrc, "w") as f:
            yaml.dump(condarc, f, indent=2)


def get_docserver_setup(public, stable, server, intranet, group):
    """Returns a setup for BOB_DOCUMENTATION_SERVER.

    What is available to build the documentation depends on the setup of
    ``public`` and ``stable``:

    * public and stable: only returns the public stable channel(s)
    * public and not stable: returns both public stable and beta channels
    * not public and stable: returns both public and private stable channels
    * not public and not stable: returns all channels

    Beta channels have priority over stable channels, if returned.  Private
    channels have priority over public channles, if turned.


    Args:

      public: Boolean indicating if we're supposed to include only public
        channels
      stable: Boolean indicating if we're supposed to include only stable
        channels
      server: The base address of the server containing our conda channels
      intranet: Boolean indicating if we should add "private"/"public" prefixes
        on the returned paths
      group: The group of packages (gitlab namespace) the package we're compiling
        is part of.  Values should match URL namespaces currently available on
        our internal webserver.  Currently, only "bob" or "beat" will work.


    Returns: a string to be used by bob.extension to find dependent
    documentation projects.
    """

    if (not public) and (not intranet):
        raise RuntimeError(
            "You cannot request for private channels and set"
            " intranet=False (server=%s) - these are conflicting options"
            % server
        )

    entries = []

    # public documentation: always can access
    prefix = "/software/%s" % group
    if stable:
        entries += [
            server + prefix + "/docs/" + group + "/%(name)s/%(version)s/",
            server + prefix + "/docs/" + group + "/%(name)s/stable/",
        ]
    else:
        entries += [server + prefix + "/docs/" + group + "/%(name)s/master/"]

    if not public:
        # add private channels, (notice they are not accessible outside idiap)
        prefix = "/private"
        if stable:
            entries += [
                server + prefix + "/docs/" + group + "/%(name)s/%(version)s/",
                server + prefix + "/docs/" + group + "/%(name)s/stable/",
            ]
        else:
            entries += [
                server + prefix + "/docs/" + group + "/%(name)s/master/"
            ]

    return "|".join(entries)


def check_version(workdir, envtag):
    """Checks if the version being built and the value reported match.

    This method will read the contents of the file ``version.txt`` and compare it
    to the potentially set ``envtag`` (may be ``None``).  If the value of
    ``envtag`` is different than ``None``, ensure it matches the value in
    ``version.txt`` or raises an exception.


    Args:

      workdir: The work directory where the repo of the package being built was
        checked-out
      envtag: (optional) tag provided by the environment


    Returns: A tuple with the version of the package that we're currently
    building and a boolean flag indicating if the version number represents a
    pre-release or a stable release.
    """

    version = open(os.path.join(workdir, "version.txt"), "rt").read().rstrip()

    # if we're building a stable release, ensure a tag is set
    parsed_version = distutils.version.LooseVersion(version).version
    is_prerelease = any([isinstance(k, str) for k in parsed_version])
    if is_prerelease:
        if envtag is not None:
            raise EnvironmentError(
                '"version.txt" indicates version is a '
                'pre-release (v%s) - but environment provided tag "%s", '
                "which indicates this is a **stable** build. "
                "Have you created the tag using ``bdt release``?"
                % (version, envtag)
            )
    else:  # it is a stable build
        if envtag is None:
            raise EnvironmentError(
                '"version.txt" indicates version is a '
                "stable build (v%s) - but there is **NO** tag environment "
                "variable defined, which indicates this is **not** "
                "a tagged build. Use ``bdt release`` to create stable releases"
                % (version,)
            )
        if envtag[1:] != version:
            raise EnvironmentError(
                '"version.txt" and the value of '
                "the provided tag do **NOT** agree - the former "
                "reports version %s, the latter, %s" % (version, envtag[1:])
            )

    return version, is_prerelease


def git_clean_build(runner, verbose):
    """Runs git-clean to clean-up build products.

    Args:

      runner: A pointer to the ``run_cmdline()`` function
      verbose: A boolean flag indicating if the git command should report erased
        files or not
    """

    # glob wild card entries we'd like to keep
    exclude_from_cleanup = [
        "miniconda.sh",  # the installer, cached
        "torch",  # eventual pytorch caches
        "sphinx",  # build artifact -- documentation
        "coverage.xml",  # build artifact -- coverage report
    ]

    # artifacts
    exclude_from_cleanup += ["miniconda/conda-bld/"]
    exclude_from_cleanup += glob.glob("dist/*.zip")

    logger.debug(
        "Excluding the following paths from git-clean:\n  - %s",
        "  - ".join(exclude_from_cleanup),
    )

    # decide on verbosity
    flags = "-ffdx"
    if not verbose:
        flags += "q"

    runner(
        ["git", "clean", flags]
        + ["--exclude=%s" % k for k in exclude_from_cleanup]
    )


def base_build(
    bootstrap,
    server,
    intranet,
    group,
    recipe_dir,
    conda_build_config,
    condarc_options,
):
    """Builds a non-beat/non-bob software dependence that doesn't exist on
    defaults.

    This function will build a software dependence that is required for our
    software stack, but does not (yet) exist on the defaults channels.  It first
    check if the build should run for the current architecture, checks if the
    package is not already built on our public channel and, if that is true, then
    proceeds with the build of the dependence.


    Args:

      bootstrap: Module that should be pre-loaded so this function can be used
        in a pre-bdt build
      server: The base address of the server containing our conda channels
      intranet: Boolean indicating if we should add "private"/"public" prefixes
        on the returned paths
      group: The group of packages (gitlab namespace) the package we're compiling
        is part of.  Values should match URL namespaces currently available on
        our internal webserver.  Currently, only "bob" or "beat" will work.
      recipe_dir: The directory containing the recipe's ``meta.yaml`` file
      conda_build_config: Path to the ``conda_build_config.yaml`` file to use
      condarc_options: Pre-parsed condarc options loaded from the respective YAML
        file


    Returns:

      list: The list of built packages, as returned by
      ``conda_build.api.build()``
    """

    # if you get to this point, tries to build the package
    channels, upload_channel = bootstrap.get_channels(
        public=True, stable=True, server=server, intranet=intranet, group=group
    )

    if "channels" not in condarc_options:
        condarc_options["channels"] = channels + ["defaults"]

    logger.info(
        "Using the following channels during (potential) build:\n  - %s",
        "\n  - ".join(condarc_options["channels"]),
    )
    logger.info("Merging conda configuration files...")
    conda_config = make_conda_config(
        conda_build_config, None, None, condarc_options
    )

    metadata = get_rendered_metadata(recipe_dir, conda_config)
    arch = conda_arch()

    # checks we should actually build this recipe
    if should_skip_build(metadata):
        logger.warn(
            'Skipping UNSUPPORTED build of "%s" on %s', recipe_dir, arch
        )
        return

    paths = get_output_path(metadata, conda_config)
    urls = [
        exists_on_channel(upload_channel, os.path.basename(k)) for k in paths
    ]

    if all(urls):
        logger.info(
            "Skipping build(s) for recipe at '%s' as packages with matching "
            "characteristics exist (%s)",
            recipe_dir,
            ", ".join(urls),
        )
        return

    if any(urls):
        use_urls = [k for k in urls if k]
        raise RuntimeError(
            "One or more packages for recipe at '%s' already exist (%s). "
            "Change the package build number to trigger a build."
            % (recipe_dir, ", ".join(use_urls)),
        )

    # if you get to this point, just builds the package(s)
    logger.info("Building %s", recipe_dir)
    with root_logger_protection():
        return conda_build.api.build(recipe_dir, config=conda_config)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Builds bob.devtools on the CI"
    )
    parser.add_argument(
        "-g",
        "--group",
        default=os.environ.get("CI_PROJECT_NAMESPACE", "bob"),
        help="The namespace of the project being built [default: %(default)s]",
    )
    parser.add_argument(
        "-n",
        "--name",
        default=os.environ.get("CI_PROJECT_NAME", "bob.devtools"),
        help="The name of the project being built [default: %(default)s]",
    )
    parser.add_argument(
        "-c",
        "--conda-root",
        default=os.environ.get(
            "CONDA_ROOT", os.path.realpath(os.path.join(os.curdir, "miniconda"))
        ),
        help="The location where we should install miniconda "
        "[default: %(default)s]",
    )
    parser.add_argument(
        "-V",
        "--visibility",
        choices=["public", "internal", "private"],
        default=os.environ.get("CI_PROJECT_VISIBILITY", "public"),
        help="The visibility level for this project [default: %(default)s]",
    )
    parser.add_argument(
        "-t",
        "--tag",
        default=os.environ.get("CI_COMMIT_TAG", None),
        help="If building a tag, pass it with this flag [default: %(default)s]",
    )
    parser.add_argument(
        "-w",
        "--work-dir",
        default=os.environ.get("CI_PROJECT_DIR", os.path.realpath(os.curdir)),
        help="The directory where the repo was cloned [default: %(default)s]",
    )
    parser.add_argument(
        "-T",
        "--twine-check",
        action="store_true",
        default=False,
        help="If set, then performs the equivalent of a "
        '"twine check" on the generated python package (zip file)',
    )
    parser.add_argument(
        "--internet",
        "-i",
        default=False,
        action="store_true",
        help="If executing on an internet-connected server, unset this flag",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Increases the verbosity level.  We always prints error and "
        "critical messages. Use a single ``-v`` to enable warnings, "
        "two ``-vv`` to enable information messages and three ``-vvv`` "
        "to enable debug messages [default: %(default)s]",
    )
    parser.add_argument(
        "--test-mark-expr",
        "-A",
        default="",
        help="Use this flag to avoid running certain tests during the build.  "
        "It forwards all settings to ``nosetests`` via --eval-attr=<settings>``"
        " and ``pytest`` via -m=<settings>.",
    )

    args = parser.parse_args()

    # loads the "adjacent" bootstrap module
    import importlib.util

    mydir = os.path.dirname(os.path.realpath(sys.argv[0]))
    bootstrap_file = os.path.join(mydir, "bootstrap.py")
    spec = importlib.util.spec_from_file_location("bootstrap", bootstrap_file)
    bootstrap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bootstrap)
    server = bootstrap._SERVER

    bootstrap.setup_logger(logger, args.verbose)

    bootstrap.set_environment("DOCSERVER", server)
    bootstrap.set_environment("LANG", "en_US.UTF-8")
    bootstrap.set_environment("LC_ALL", os.environ["LANG"])
    bootstrap.set_environment("NOSE_EVAL_ATTR", args.test_mark_expr)
    bootstrap.set_environment("PYTEST_ADDOPTS", f"-m '{args.test_mark_expr}'")

    # get information about the version of the package being built
    version, is_prerelease = check_version(args.work_dir, args.tag)
    bootstrap.set_environment("BOB_PACKAGE_VERSION", version)

    # create the build configuration
    conda_build_config = os.path.join(
        args.work_dir, "conda", "conda_build_config.yaml"
    )
    recipe_append = os.path.join(args.work_dir, "data", "recipe_append.yaml")

    condarc = os.path.join(args.conda_root, "condarc")
    logger.info("Loading (this build's) CONDARC file from %s...", condarc)
    with open(condarc, "rb") as f:
        condarc_options = yaml.load(f, Loader=yaml.FullLoader)

    # dump packages at conda_root
    prefix = get_env_directory(os.environ["CONDA_EXE"], "base")
    if condarc_options.get("conda-build", {}).get("root-dir") is None:
        condarc_options["croot"] = os.path.join(prefix, "conda-bld")

    # builds all dependencies in the 'deps' subdirectory - or at least checks
    # these dependencies are already available; these dependencies go directly
    # to the public channel once built
    recipes = load_order_file(os.path.join("deps", "order.txt"))
    for k, recipe in enumerate([os.path.join("deps", k) for k in recipes]):

        if not os.path.exists(os.path.join(recipe, "meta.yaml")):
            # ignore - not a conda package
            continue
        base_build(
            bootstrap,
            server,
            not args.internet,
            args.group,
            recipe,
            conda_build_config,
            condarc_options,
        )

    public = args.visibility == "public"
    channels, upload_channel = bootstrap.get_channels(
        public=public,
        stable=(not is_prerelease),
        server=server,
        intranet=(not args.internet),
        group=args.group,
    )

    if "channels" not in condarc_options:
        condarc_options["channels"] = channels + ["defaults"]

    logger.info(
        "Using the following channels during build:\n  - %s",
        "\n  - ".join(condarc_options["channels"]),
    )
    logger.info("Merging conda configuration files...")
    conda_config = make_conda_config(
        conda_build_config, None, recipe_append, condarc_options
    )

    recipe_dir = os.path.join(args.work_dir, "conda")
    metadata = get_rendered_metadata(recipe_dir, conda_config)
    paths = get_output_path(metadata, conda_config)

    # asserts we're building at the right location
    for path in paths:
        assert path.startswith(os.path.join(args.conda_root, "conda-bld")), (
            'Output path for build (%s) does not start with "%s" - this '
            "typically means this build is running on a shared builder and "
            "the file ~/.conda/environments.txt is polluted with other "
            "environment paths.  To fix, empty that file and set its mode "
            "to read-only for all."
            % (path, os.path.join(args.conda_root, "conda-bld"))
        )

    # retrieve the current build number(s) for this build
    build_numbers = [
        next_build_number(upload_channel, os.path.basename(k))[0] for k in paths
    ]

    # homogenize to the largest build number
    build_number = max([int(k) for k in build_numbers])

    # runs the build using the conda-build API
    arch = conda_arch()

    # notice we cannot build from the pre-parsed metadata because it has already
    # resolved the "wrong" build number.  We'll have to reparse after setting the
    # environment variable BOB_BUILD_NUMBER.
    bootstrap.set_environment("BOB_BUILD_NUMBER", str(build_number))
    with root_logger_protection():
        conda_build.api.build(recipe_dir, config=conda_config)

    # checks if long_description of python package renders fine
    if args.twine_check:
        from twine.commands.check import check

        package = glob.glob("dist/*.zip")
        failed = check(package)

        if failed:
            raise RuntimeError(
                "twine check (a.k.a. readme check) %s: FAILED" % package[0]
            )
        else:
            logger.info("twine check (a.k.a. readme check) %s: OK", package[0])

    git_clean_build(bootstrap.run_cmdline, verbose=(args.verbose >= 3))
