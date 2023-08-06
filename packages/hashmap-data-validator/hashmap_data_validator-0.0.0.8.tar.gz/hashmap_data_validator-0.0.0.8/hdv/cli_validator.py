import click
from hdv.validator import Validator


@click.command()
@click.option('-sf', '--snowflake_table', required=False, help='Snowflake table to be validated')
@click.option('-jdbc', '--jdbc_table', required=False, help='JDBC table to be validated')
@click.option("--jdbc_sql", required=False, help='Run your own sql query inside your JDBC database instead of the default.')
@click.option("--sf_sql", required=False, help='Run your own sql query inside your Snowflake database instead of the default.')
def cli_validate(snowflake_table: str = None, jdbc_table: str = None, jdbc_sql: str = None, sf_sql: str = None):
    """ - makes hdv method callable via cli
        - configured in setup.py to be callable with 'hdv' command """

    # Validator instance
    cli_validation = Validator()

    # calls hdv method from cli
    cli_validation.hdv(snowflake_table=snowflake_table, jdbc_table=jdbc_table, jdbc_query=jdbc_sql, sf_query=sf_sql)
