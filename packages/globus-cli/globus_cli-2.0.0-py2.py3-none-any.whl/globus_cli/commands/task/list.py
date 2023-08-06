import click

from globus_cli.parsing import command
from globus_cli.safeio import formatted_print
from globus_cli.services.transfer import get_client, iterable_response_to_dict


def _format_date_callback(ctx, param, value):
    if value is None:
        return ""
    return value.strftime("%Y-%m-%d %H:%M:%S")


@command(
    "list",
    short_help="List your tasks",
    adoc_output="""When text output is requested, the following fields are used:

- 'Task ID'
- 'Status'
- 'Type'
- 'Source Display Name'
- 'Dest Display Name'
- 'Label'
""",
    adoc_examples="""List results in a text table:

[source,bash]
----
$ globus task list
----

List the first 100 tasks which were completed between May 2015 and July 2015,
but whose labels aren't the exact string 'autolabel':

[source,bash]
----
$ globus task list --limit 100 \
    --filter-completed-after 2015-05-01 \
    --filter-completed-before 2015-07-30 \
    --filter-not-label 'autolabel' --exact
----

List active transfers in a tabular format suitable for consumption by unix
tools:

[source,bash]
----
$ globus task list --format unix \
    --jmespath 'DATA[?status==`ACTIVE`].[task_id, source_endpoint_id, destination_endpoint_id, label]'
----

NOTE: 'destination_endpoint_id' will be 'None' in the case of Delete tasks.

Cancel all tasks with expired credentials:

[source,bash]
----
# careful: do not quote this output, but instead rely on the shell's
# word-splitting for this for-loop
for id in $(globus task list --filter-status=INACTIVE \
                             --format=UNIX \
                             --jmespath='DATA[*].task_id'); do
    globus task cancel $id
done
----

Print out task statuses with links to their pages in the web UI:

[source,bash]
----
globus task list --format=unix --jmespath='DATA[*].[task_id, status]' | \
    awk '{printf "Task %s is currently %s\n", $1, $2;
          printf "View at https://app.globus.org/activity/%s\n\n", $1}'
----
""",  # noqa: E501
)
@click.option("--limit", default=10, show_default=True, help="Limit number of results.")
@click.option(
    "--filter-task-id",
    multiple=True,
    type=click.UUID,
    help="task UUID to filter by. This option can be used multiple times.",
)
@click.option(
    "--filter-type",
    type=click.Choice(["TRANSFER", "DELETE"]),
    help="Filter results to only TRANSFER or DELETE tasks.",
)
@click.option(
    "--filter-status",
    multiple=True,
    type=click.Choice(["ACTIVE", "INACTIVE", "FAILED", "SUCCEEDED"]),
    help="Task status to filter results by. This option can be used multiple times.",
)
@click.option(
    "--filter-label",
    multiple=True,
    help=(
        "Filter results to task whose label matches pattern. "
        "This option can be used multiple times."
    ),
)
@click.option(
    "--filter-not-label",
    multiple=True,
    help=(
        "Filter not results whose label matches pattern. "
        "This option can be used multiple times."
    ),
)
@click.option(
    "--inexact / --exact",
    default=True,
    help=(
        "Allows / disallows --filter-label and --filter-not-label to use "
        "'*' as a wild-card character and ignore case"
    ),
)
@click.option(
    "--filter-requested-after",
    type=click.DateTime(),
    callback=_format_date_callback,
    help="Filter results to tasks that were requested after given time.",
)
@click.option(
    "--filter-requested-before",
    type=click.DateTime(),
    callback=_format_date_callback,
    help="Filter results to tasks that were requested before given time.",
)
@click.option(
    "--filter-completed-after",
    type=click.DateTime(),
    callback=_format_date_callback,
    help="Filter results to tasks that were completed after given time.",
)
@click.option(
    "--filter-completed-before",
    type=click.DateTime(),
    callback=_format_date_callback,
    help="Filter results to tasks that were completed before given time.",
)
def task_list(
    limit,
    filter_task_id,
    filter_status,
    filter_type,
    filter_label,
    filter_not_label,
    inexact,
    filter_requested_after,
    filter_requested_before,
    filter_completed_after,
    filter_completed_before,
):
    """
    List tasks for the current user.

    This lists your most recent tasks. The tasks displayed may be filtered by a number
    of attributes, each with a separate commandline option.
    """

    def _process_filterval(prefix, value, default=None):
        if value:
            if isinstance(value, str):
                return f"{prefix}:{value}/"
            return "{}:{}/".format(prefix, ",".join(str(x) for x in value))
        else:
            return default or ""

    # make filter string
    filter_string = ""
    filter_string += _process_filterval("task_id", filter_task_id)
    filter_string += _process_filterval("status", filter_status)
    filter_string += _process_filterval(
        "type", filter_type, default="type:TRANSFER,DELETE/"
    )

    # combine data into one list for easier processing
    if inexact:
        label_data = ["~" + s for s in filter_label] + [
            "!~" + s for s in filter_not_label
        ]
    else:
        label_data = ["=" + s for s in filter_label] + [
            "!" + s for s in filter_not_label
        ]
    filter_string += _process_filterval("label", label_data)

    filter_string += _process_filterval(
        "request_time", [filter_requested_after, filter_requested_before]
    )
    filter_string += _process_filterval(
        "completion_time", [filter_completed_after, filter_completed_before]
    )

    client = get_client()
    task_iterator = client.task_list(
        num_results=limit, filter=filter_string[:-1]
    )  # ignore trailing /

    fields = [
        ("Task ID", "task_id"),
        ("Status", "status"),
        ("Type", "type"),
        ("Source Display Name", "source_endpoint_display_name"),
        ("Dest Display Name", "destination_endpoint_display_name"),
        ("Label", "label"),
    ]
    formatted_print(
        task_iterator, fields=fields, json_converter=iterable_response_to_dict
    )
