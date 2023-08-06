import click
from globus_sdk import DeleteData

from globus_cli.parsing import (
    ENDPOINT_PLUS_REQPATH,
    command,
    delete_and_rm_options,
    synchronous_task_wait_options,
    task_submission_options,
)
from globus_cli.safeio import err_is_terminal, formatted_print, term_is_interactive
from globus_cli.services.transfer import autoactivate, get_client, task_wait_with_io


@command(
    "rm",
    short_help="Delete a single path; wait for it to complete",
    adoc_examples="""Delete a single file.

[source,bash]
----
$ ep_id=ddb59af0-6d04-11e5-ba46-22000b92c6ec
$ globus rm $ep_id:~/myfile.txt
----

Delete a directory recursively.

[source,bash]
----
$ ep_id=ddb59af0-6d04-11e5-ba46-22000b92c6ec
$ globus rm $ep_id:~/mydir --recursive
----
""",
)
@task_submission_options
@delete_and_rm_options(supports_batch=False, default_enable_globs=True)
@synchronous_task_wait_options
@click.argument("endpoint_plus_path", type=ENDPOINT_PLUS_REQPATH)
def rm_command(
    ignore_missing,
    star_silent,
    recursive,
    enable_globs,
    endpoint_plus_path,
    label,
    submission_id,
    dry_run,
    deadline,
    skip_activation_check,
    notify,
    meow,
    heartbeat,
    polling_interval,
    timeout,
    timeout_exit_code,
):
    """
    Submit a Delete Task to delete a single path, and then block and wait for it to
    complete.

    Output is similar to *globus task wait*, and it is safe to *globus task wait*
    on a *globus rm* which timed out.

    Symbolic links are never followed - only unlinked (deleted).

    {AUTOMATIC_ACTIVATION}
    """
    endpoint_id, path = endpoint_plus_path

    client = get_client()

    # attempt to activate unless --skip-activation-check is given
    if not skip_activation_check:
        autoactivate(client, endpoint_id, if_expires_in=60)

    delete_data = DeleteData(
        client,
        endpoint_id,
        label=label,
        recursive=recursive,
        ignore_missing=ignore_missing,
        submission_id=submission_id,
        deadline=deadline,
        skip_activation_check=skip_activation_check,
        interpret_globs=enable_globs,
        **notify
    )

    if not star_silent and enable_globs and path.endswith("*"):
        # not intuitive, but `click.confirm(abort=True)` prints to stdout
        # unnecessarily, which we don't really want...
        # only do this check if stderr is a pty
        if (
            err_is_terminal()
            and term_is_interactive()
            and not click.confirm(
                'Are you sure you want to delete all files matching "{}"?'.format(path),
                err=True,
            )
        ):
            click.echo("Aborted.", err=True)
            click.get_current_context().exit(1)
    delete_data.add_item(path)

    if dry_run:
        formatted_print(delete_data, response_key="DATA", fields=[("Path", "path")])
        # exit safely
        return

    # Print task submission to stderr so that `-Fjson` is still correctly
    # respected, as it will be by `task wait`
    res = client.submit_delete(delete_data)
    task_id = res["task_id"]
    click.echo('Delete task submitted under ID "{}"'.format(task_id), err=True)

    # do a `task wait` equivalent, including printing and correct exit status
    task_wait_with_io(
        meow,
        heartbeat,
        polling_interval,
        timeout,
        task_id,
        timeout_exit_code,
        client=client,
    )
