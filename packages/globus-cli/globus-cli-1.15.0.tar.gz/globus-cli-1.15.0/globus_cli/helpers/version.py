import platform
import site
import sys

import click

from globus_cli.safeio import is_verbose, verbosity
from globus_cli.version import get_versions


def _get_package_data():
    """
    Import a set of important packages and return relevant data about them in a
    dict.
    Imports are done in here to avoid potential for circular imports and other
    problems, and to make iteration simpler.
    """
    moddata = []
    modlist = (
        "click",
        "configobj",
        "cryptography",
        "globus_cli",
        "globus_sdk",
        "jmespath",
        "requests",
        "six",
    )
    if verbosity() < 2:
        modlist = ("globus_cli", "globus_sdk", "requests")

    for mod in modlist:
        cur = [mod]
        try:
            loaded_mod = __import__(mod)
        except ImportError:
            loaded_mod = None

        for attr in ("__version__", "__file__", "__path__"):
            # if loading failed, be sure to pad with error messages
            if loaded_mod is None:
                cur.append("[import failed]")
                continue

            try:
                attrval = getattr(loaded_mod, attr)
            except AttributeError:
                attrval = ""
            cur.append(attrval)
        moddata.append(cur)

    return moddata


def _get_versionblock_message(current, latest, upgrade_target):
    if latest == upgrade_target:
        return """\
Installed version:  {}
Latest version:     {}""".format(
            current, latest
        )
    # latest != upgrade_target means it's a py2 environment where we're capped at <2.0
    else:
        return """\
You are running the Globus CLI on python2

Installed version:           {}
Latest version for python2:  {}
Latest version for python3:  {}""".format(
            current, upgrade_target, latest
        )


def _get_post_message(current, latest, upgrade_target):
    if current == latest:
        return "You are running the latest version of the Globus CLI"
    if current > latest:
        return "You are running a preview version of the Globus CLI"
    if upgrade_target == latest:
        return "You should update your version of the Globus CLI with\n  globus update"
    if current == upgrade_target:
        return """\
You are running the latest version of the Globus CLI supported by python2.

To upgrade to the latest version of the CLI ({}), you will need to
uninstall and reinstall the CLI using python3.""".format(
            latest
        )
    if current < upgrade_target:
        return """\
You should update your version of the Globus CLI.
However, your python2 runtime does not support the latest version.

You may update with the 'globus update' command, but we recommend that
you uninstall and reinstall the CLI using python3."""
    # should be unreachable
    return "Unrecognized status. You may be on a development version."


def print_version():
    """
    Print out the current version, and at least try to fetch the latest from
    PyPi to print alongside it.

    It may seem odd that this isn't in globus_cli.version , but it's done this
    way to separate concerns over printing the version from looking it up.
    """
    upgrade_target, latest, current = get_versions()
    if latest is None:
        click.echo(
            ("Installed Version: {0}\nFailed to lookup latest version.").format(current)
        )
    else:
        click.echo(
            _get_versionblock_message(current, latest, upgrade_target)
            + "\n\n"
            + _get_post_message(current, latest, upgrade_target)
        )

    # verbose shows more platform and python info
    # it also includes versions of some CLI dependencies
    if is_verbose():
        moddata = _get_package_data()

        click.echo("\nVerbose Data\n---")

        click.echo("platform:")
        click.echo("  platform: {}".format(platform.platform()))
        click.echo("  py_implementation: {}".format(platform.python_implementation()))
        click.echo("  py_version: {}".format(platform.python_version()))
        click.echo("  sys.executable: {}".format(sys.executable))
        click.echo("  site.USER_BASE: {}".format(site.USER_BASE))

        click.echo("modules:")
        for mod, modversion, modfile, modpath in moddata:
            click.echo("  {}:".format(mod))
            click.echo("    __version__: {}".format(modversion))
            click.echo("    __file__: {}".format(modfile))
            click.echo("    __path__: {}".format(modpath))
