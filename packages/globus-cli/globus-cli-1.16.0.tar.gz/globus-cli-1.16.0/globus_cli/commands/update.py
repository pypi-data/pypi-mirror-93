import atexit
import site
import subprocess
import sys

import click

from globus_cli.parsing import command
from globus_cli.version import get_versions

# check if the source for this is inside of the USER_BASE
# if so, a `pip install --user` was used
# https://docs.python.org/2/library/site.html#site.USER_BASE
IS_USER_INSTALL = __file__.startswith(site.USER_BASE)


def _call_pip(*args):
    """
    Invoke pip *safely* and in the *supported* way:
    https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program
    """
    all_args = [sys.executable, "-m", "pip"] + list(args)
    print("> {}".format(" ".join(all_args)))
    subprocess.check_call(all_args)


def _check_pip_installed():
    """
    Invoke `pip --version` and make sure it doesn't error.
    Use check_output to capture stdout and stderr

    Invokes pip by the same manner that we plan to in _call_pip()

    Don't bother trying to reuse _call_pip to do this... Finnicky and not worth
    the effort.
    """
    try:
        subprocess.check_output(
            [sys.executable, "-m", "pip", "--version"], stderr=subprocess.STDOUT
        )
        return True
    except subprocess.CalledProcessError:
        return False


@command(
    "update",
    disable_options=["format", "map_http_status"],
    short_help="Update the Globus CLI to its  latest version",
)
@click.option("--yes", is_flag=True, help='Automatically say "yes" to all prompts')
# hidden options to fetch branches or tags from GitHub. One turns this mode
# on or off, and the other is used to set a non-main target
# --development-version implies --development
@click.option("--development", is_flag=True, hidden=True)
@click.option("--development-version", hidden=True, default=None)
def update_command(yes, development, development_version):
    """Update the Globus CLI to its latest version.

    NOTE: This command requires having pip. If you used an alternative method
    of installing the Globus CLI you can install pip to run this command,
    or manually update the Globus CLI using the method you used for install.

    The *globus update* command checks if a more recent version of the Globus CLI
    is available on PyPi, and if so asks for user consent to update to the most
    recent version available.
    """
    # enforce that pip MUST be installed
    # Why not just include it in the setup.py requirements? Mostly weak
    # reasons, but it shouldn't matter much.
    # - if someone has installed the CLI without pip, then they haven't
    #   followed our install instructions, so it's mostly a non-issue
    # - we don't want to have `pip install -U globus-cli` upgrade pip -- that's
    #   a little bit invasive and easy to do by accident on modern versions of
    #   pip where `--upgrade-strategy` defaults to `eager`
    # - we may want to do distributions in the future with dependencies baked
    #   into a package, but we'd never want to do that with pip. More changes
    #   would be needed to support that use-case, which we've discussed, but
    #   not depending directly on pip gives us a better escape hatch
    # - if we depend on pip, we need to start thinking about what versions we
    #   support. In point of fact, that becomes an issue as soon as we add this
    #   command, but not being explicit about it lets us punt for now (maybe
    #   indefinitely) on figuring out version requirements. All of that is to
    #   say: not including it is bad, and from that badness we reap the rewards
    #   of procrastination and non-explicit requirements
    # - Advanced usage, like `pip install -t` can produce an installed version
    #   of the CLI which can't import its installing `pip`. If we depend on
    #   pip, anyone doing this is forced to get two copies of pip, which seems
    #   kind of nasty (even if "they're asking for it")
    if not _check_pip_installed():
        click.echo("`globus update` requires pip. Please install pip and try again")
        click.get_current_context().exit(1)

    # --development-version implies --development
    development = development or (development_version is not None)

    # if we're running with `--development`, then the target version is a
    # tarball from GitHub, and we can skip out on the safety checks
    if development:
        # default to main
        development_version = development_version or "main"
        target_version = (
            "https://github.com/globus/globus-cli/archive/{}.tar.gz#egg=globus-cli"
        ).format(development_version)
    else:
        # lookup version from PyPi, abort if we can't get it
        upgrade_target, latest, current = get_versions()
        if latest is None:
            click.echo("Failed to lookup latest version. Aborting.")
            click.get_current_context().exit(1)

        # in the case where we're already up to date, do nothing and exit
        if current == latest:
            click.echo("You are already running the latest version: {}".format(current))
            return

        # we are not all the way up to date (did not match `latest`) but we match the
        # latest version supported by the current platform/runtime . So exit 0 with a
        # warning
        if current == upgrade_target:
            if upgrade_target != latest:
                click.echo(
                    click.style(
                        (
                            "You are running the latest version ({}) supported by "
                            "python2.\n"
                            "However, a newer version ({}) is available.\n"
                            "If you would like to update to the latest version, you "
                            "need to reinstall globus-cli using python3."
                        ).format(upgrade_target, latest),
                        fg="yellow",
                    )
                )
            return

        # show the version(s) and prompt to continue
        explain_upgrade = "The latest version is {}".format(latest)
        if upgrade_target != latest:
            explain_upgrade = """\
The latest version for python2 is {0}
The latest version for python3 is {1}.
If you would like to install version {1}, you must reinstall globus-cli using python3.
""".format(
                upgrade_target, latest
            )
        click.echo(
            "You are already running version {}\n" "{}".format(current, explain_upgrade)
        )
        if not yes and (not click.confirm("Continue with the upgrade?", default=True)):
            click.get_current_context().exit(1)

        # if we make it through to here, it means we didn't hit any safe (or
        # unsafe) abort conditions, so set the target version for upgrade to
        # the latest
        target_version = "globus-cli=={}".format(upgrade_target)

    # print verbose warning/help message, to guide less fortunate souls who hit
    # Ctrl+C at a foolish time, lose connectivity, or don't invoke with `sudo`
    # on a global install of the CLI
    click.echo(
        (
            "The Globus CLI will now update itself.\n"
            "In the event that an error occurs or the update is interrupted, we "
            "recommend uninstalling and reinstalling the CLI.\n"
            "Update Target: {}\n"
        ).format(target_version)
    )

    # register the upgrade activity as an atexit function
    # this ensures that most library teardown (other than whatever libs might
    # jam into atexit themselves...) has already run, and therefore protects us
    # against most potential bugs resulting from upgrading click while a click
    # command is running
    #
    # NOTE: there is a risk that we will see bugs on upgrade if the act of
    # doing a pip upgrade install changes state on disk and we (or a lib we
    # use) rely on that via pkg_resources, lazy/deferred imports, or good
    # old-fashioned direct inspection of `__file__` and the like DURING an
    # atexit method. Anything outside of atexit methods remains safe!
    @atexit.register
    def do_upgrade():
        install_args = ["install", "--upgrade", target_version]
        if IS_USER_INSTALL:
            install_args.insert(1, "--user")
        _call_pip(*install_args)
