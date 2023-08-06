#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import click
import yaml

from ..config import read_config
from ..bootstrap import set_environment
from ..bootstrap import run_cmdline
from ..build import conda_create
from ..build import make_conda_config
from ..build import parse_dependencies
from ..constants import BASE_CONDARC
from ..constants import CONDA_BUILD_CONFIG
from ..constants import CONDA_RECIPE_APPEND
from ..constants import SERVER
from ..log import echo_normal
from ..log import get_logger
from ..log import verbosity_option
from . import bdt

logger = get_logger(__name__)


def _uniq(seq):
    """Fast order preserving uniq() function for Python lists"""

    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


@click.command(
    epilog="""
Examples:

  1. Creates an environment called `myenv' for developing the currently checked-out package (N.B.: first activate the base environment):

\b
     $ cd bob.package.foo
     $ bdt create -vv myenv

     The above command assumes the directory `conda' exists on the current directory and that it contains a file called `meta.yaml' containing the recipe for the package you want to create a development environment for.

     If you get things right by default, the above form is the typical usage scenario of this app. Read-on to tweak special flags and settings.


  2. By default, we use the native python version of your conda installation as the default python version to use for the newly created environment. You may select a different one with `--python=X.Y':

     $ bdt create -vv --python=3.6 myenv


  3. By default, we use our own condarc and `conda_build_config.yaml` files that are used in creating packages for our CI/CD system. If you wish to use your own, specify them on the command line:

     $ bdt create -vv --python=3.6 --config=config.yaml --condarc=~/.condarc myenv

     Notice the condarc file **must** end in `condarc', or conda will complain.


  4. You can use the option `--dry-run' to simulate what would be installed
  instead of actually creating a new environment.  Combine with `-vvv` to
  enable debug printing.  Equivalent conda commands you can execute on the
  shell will be printed:

     $ bdt create -vvv --dry-run myenv


  5. You can use the option `--pip-extras` to force the installation of extra
  Python packages that are useful in your development environment.  By default
  we do not install anything, but you may configure this via this flag, or
  through the configuration file option `create/pip_extras` to do so, as
  explained in our Setup subsection of the Installation manual.  To use this
  flag on the command-line, specify one pip-installable package each time:

     $ bdt create -vvv --pip-extras=ipdb --pip-extras=mr.developer myenv

     Using this option **adds** to what is available in the configuration file.
     So, if your configuration file already contains ``ipdb`` and you wish to
     install ``mr.developer`` as a plus, then just specify
     ``--pip-extras=mr.developer``.

"""
)
@click.argument("name")
@click.argument(
    "recipe-dir",
    required=False,
    type=click.Path(file_okay=False, dir_okay=True, exists=True),
)
@click.option(
    "-p",
    "--python",
    default=("%d.%d" % sys.version_info[:2]),
    show_default=True,
    help="Version of python to build the "
    "environment for [default: %(default)s]",
)
@click.option(
    "-o",
    "--overwrite/--no-overwrite",
    default=False,
    help="If set and an environment with the same name exists, "
    "deletes it first before creating the new environment",
    show_default=True,
)
@click.option(
    "-r",
    "--condarc",
    help="Use custom conda configuration file instead of our own",
)
@click.option(
    "-l",
    "--use-local",
    default=False,
    help="Allow the use of local channels for package retrieval",
)
@click.option(
    "-m",
    "--config",
    "--variant-config-files",
    show_default=True,
    default=CONDA_BUILD_CONFIG,
    help="overwrites the path leading to " "variant configuration file to use",
)
@click.option(
    "-a",
    "--append-file",
    show_default=True,
    default=CONDA_RECIPE_APPEND,
    help="overwrites the path leading to " "appended configuration file to use",
)
@click.option(
    "-S",
    "--server",
    show_default=True,
    default=SERVER,
    help="Server used for downloading conda packages and documentation "
    "indexes of required packages",
)
@click.option(
    "-g",
    "--group",
    show_default=True,
    default="bob",
    help="Group of packages (gitlab namespace) this package belongs to",
)
@click.option(
    "-P",
    "--private/--no-private",
    default=False,
    help="Set this to **include** private channels on your build - "
    "you **must** be at Idiap to execute this build in this case - "
    "you **must** also use the correct server name through --server - "
    "notice this option has no effect if you also pass --condarc",
)
@click.option(
    "-X",
    "--stable/--no-stable",
    default=False,
    help="Set this to **exclude** beta channels from your build - "
    "notice this option has no effect if you also pass --condarc",
)
@click.option(
    "-d",
    "--dry-run/--no-dry-run",
    default=False,
    help="Only goes through the actions, but does not execute them "
    "(combine with the verbosity flags - e.g. ``-vvv``) to enable "
    "printing to help you understand what will be done",
)
@click.option(
    "-x",
    "--pip-extras",
    multiple=True,
    default=[],
    help="Using pip, installs this additional list of dependencies to "
    "created environments.  Pip installation happens after the base conda "
    "install (defaults, if any, are listed in ~/.bdtrc)",
)
@verbosity_option()
@bdt.raise_on_error
def create(
    name,
    recipe_dir,
    python,
    overwrite,
    condarc,
    use_local,
    config,
    append_file,
    server,
    group,
    private,
    stable,
    dry_run,
    pip_extras,
):
    """Creates a development environment for a recipe.

    It uses the conda render API to render a recipe and install an environment
    containing all build/host, run and test dependencies of a package. It does
    **not** build the package itself, just install dependencies so you can build
    the package by hand, possibly using buildout or similar. If you'd like to
    conda-build your package, just use `conda build` instead.

    Once the environment is created, a copy of the used `condarc' file is placed
    on the root of the environment. Installing or updating packages on the newly
    created environment should be possible without further configuration. Notice
    that beta packages quickly get outdated and upgrading may no longer be
    possible for aging development environments. You're advised to always re-use
    this app and use the flag `--overwrite` to re-create from scratch the
    development environment.
    """

    recipe_dir = recipe_dir or os.path.join(os.path.realpath("."), "conda")

    if not os.path.exists(recipe_dir):
        raise RuntimeError("The directory %s does not exist" % recipe_dir)

    # this is not used to conda-build, just to create the final environment
    conda = os.environ.get("CONDA_EXE")
    if conda is None:
        raise RuntimeError(
            "Cannot find `conda' executable (${CONDA_EXEC}) - "
            "have you activated the build environment containing bob.devtools "
            "properly?"
        )

    # set some environment variables before continuing
    set_environment("DOCSERVER", server, os.environ)
    set_environment("NOSE_EVAL_ATTR", "", os.environ)
    set_environment("PYTEST_ADDOPTS", "", os.environ)

    logger.debug(
        'This package is considered part of group "%s" - tunning '
        "conda package URLs for this...",
        group,
    )

    if condarc is not None:
        logger.info("Loading CONDARC file from %s...", condarc)
        with open(condarc, "rb") as f:
            condarc_options = yaml.load(f, Loader=yaml.FullLoader)
    else:
        # use default
        condarc_options = yaml.load(BASE_CONDARC, Loader=yaml.FullLoader)

    if "channels" not in condarc_options:
        from ..bootstrap import get_channels

        channels, _ = get_channels(
            public=(not private),
            stable=stable,
            server=server,
            intranet=private,
            group=group,
        )
        condarc_options["channels"] = channels + ["defaults"]

    logger.info(
        "Using the following channels during environment creation:" "\n  - %s",
        "\n  - ".join(condarc_options["channels"]),
    )

    conda_config = make_conda_config(
        config, python, append_file, condarc_options
    )
    deps = parse_dependencies(recipe_dir, conda_config)
    # when creating a local development environment, remove the always_yes
    # option

    del condarc_options["always_yes"]
    conda_create(
        conda, name, overwrite, condarc_options, deps, dry_run, use_local
    )

    # part 2: pip-install everything listed in pip-extras
    # mix-in stuff from ~/.bdtrc and command-line
    config = read_config()
    pip_extras_config = []
    if "create" in config:
        pip_extras_config = config["create"].get("pip_extras", "").split()
    pip_extras = _uniq(pip_extras_config + list(pip_extras))
    logger.info("Pip-installing: %s", pip_extras)

    cmd = [conda, "run", "--live-stream", "--name", name, "pip", "install"]
    cmd += pip_extras
    if not dry_run:
        run_cmdline(cmd)
    else:
        logger.info(f"Command: {' '.join(cmd)}")

    echo_normal(f'>>> Execute on your shell: "conda activate {name}"')
