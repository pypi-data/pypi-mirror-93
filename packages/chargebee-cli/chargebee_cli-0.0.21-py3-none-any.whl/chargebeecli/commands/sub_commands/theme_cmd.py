import click

from chargebeecli.constants.constants import Formats, Export_Formats
from chargebeecli.processors.themes.theme import Theme


@click.command("theme", help='themes for cli')
@click.pass_context
@click.option("--id", "-i", help="event id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
def cmd(ctx, id, operation):
    Theme(export_format=None, export_path=None, file_name=None,
          response_format=Formats.TABLE.value, _operation=operation, _input_columns=None) \
        .process(None, operation, payload=None, resource_id=id) \
        .format() \
        .export_data() \
        .print_response()


@click.command("apply", help='themes for cli')
@click.pass_context
@click.option("--id", "-i", help="event id", required=False, type=str)
@click.option("--operation", "-op", required=True,
              help=" operation to be executed, like fetch/create/update/delete.. ")
@click.option('--columns', '-cols', nargs=0, required=False, help="columns to be printed in output")
@click.option("--format", "-f", required=False,
              help="this allows user to format the output in json or table format..", default=Formats.TABLE.name)
@click.argument('columns', nargs=-1)
@click.option('--export-format', "-ef", help='data to be imported in [csv / excel / html',
              default=Export_Formats.CSV.value, type=str)
@click.option('--export-filename', "-efn", help='name of exported file', type=str)
@click.option('--export-path', "-ep", help='path where file to be exported', type=click.Path(exists=True))
def theme_apply(ctx, id, operation, columns, format, export_filename, export_format, export_path):
    Theme(export_format=export_format, export_path=export_path, file_name=export_filename,
          response_format=format, _operation=operation, _input_columns=columns) \
        .process(None, operation, payload=None, resource_id=id) \
        .format() \
        .export_data() \
        .print_response()
