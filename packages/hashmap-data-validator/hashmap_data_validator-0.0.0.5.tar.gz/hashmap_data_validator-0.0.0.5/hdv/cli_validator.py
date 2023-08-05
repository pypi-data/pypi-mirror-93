import click
from hdv.validator import Validator


@click.command()
@click.option('-sf', '--snowflake_table', required=True, help='Snowflake table to be validated')
@click.option('-jdbc', '--jdbc_table', required=True, help='JDBC table to be validated')
def cli_validate(snowflake_table: str, jdbc_table: str):
    """ - makes hdv method callable via cli
        - configured in setup.py to be callable with 'hdv' command """

    # Validator instance
    cli_validation = Validator()

    # calls hdv method from cli
    cli_validation.hdv(snowflake_table=snowflake_table, jdbc_table=jdbc_table)
