from hdv.validator import Validator

s = Validator()

s.hdv(jdbc_table='validator', snowflake_table='COPY_SNOWFLAKE_TEST')