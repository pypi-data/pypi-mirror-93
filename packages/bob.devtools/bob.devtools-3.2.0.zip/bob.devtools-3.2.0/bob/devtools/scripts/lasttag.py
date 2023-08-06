#!/usr/bin/env python

import click
import gitlab

from ..changelog import get_last_tag
from ..changelog import parse_date
from ..log import echo_normal
from ..log import echo_warning
from ..log import get_logger
from ..log import verbosity_option
from ..release import get_gitlab_instance
from . import bdt

logger = get_logger(__name__)


@click.command(
    epilog="""
Examples:

  1. Get the last tag information of the bob/bob package

     $ bdt gitlab lasttag bob/bob


  2. Get the last tag information of the beat/beat.core package

     $ bdt gitlab lasttag beat/beat.core

"""
)
@click.argument("package")
@verbosity_option()
@bdt.raise_on_error
def lasttag(package):
    """Returns the last tag information on a given PACKAGE."""

    if "/" not in package:
        raise RuntimeError('PACKAGE should be specified as "group/name"')

    gl = get_gitlab_instance()

    # we lookup the gitlab package once
    try:
        use_package = gl.projects.get(package)
        logger.info(
            "Found gitlab project %s (id=%d)",
            use_package.attributes["path_with_namespace"],
            use_package.id,
        )

        tag = get_last_tag(use_package)
        date = parse_date(tag.commit["committed_date"])
        echo_normal(
            "%s: %s (%s)" % (package, tag.name, date.strftime("%Y-%m-%d %H:%M:%S"))
        )
    except gitlab.GitlabGetError:
        logger.warn(
            "Gitlab access error - package %s does not exist?", package, exc_info=True
        )
        echo_warning("%s: unknown" % (package,))
