# Hashmap Data Validator

## MVP
This repo holds the hashmap-data-validator. Hashmap-data-validator is a tool used for data validation between a JDBC connectable database and a Snowflake database.

## How it works
HDV uses great expectations to run validation on the two tables. It currently runs expectations on row
count and row hash values to validate the tables. The main `hdv` method can be found in `validator.py`. It is imported inside `__init__.py` and therefore
the user can import the method in their own project. 

The `hdv` command line method is configured in `cli_validator.py`. It uses the python `Click` library with `setuptools` to be callable via the CLI.
## How to use
* The user installs the package via PyPi with ```pip install hashmap-data-validator```
* After installation, user needs to run a `.py` file with the following import: `from hdv import hdv`
* A `.yml` file will then be created in the user's `home` directory with the following path: `.hashmap_data_validator/hdv_profiles.yml`
* The user then configures their JDBC and Snowflake credentials in the `.yml`. HDV uses this file to manage the JDBC and Snowflake connections for the user.
* After configuration is complete, the user can call `hdv` two different ways:
    1. From the command line
    2. From a python file as an imported method
    
### API
#### `hdv` called via imported python method
```python
hdv(
    jdbc_table: str, 
    snowflake_table: str, 
    snowflake_database: str = None,
    snowflake_schema: str = None, 
    jdbc_database: str = None
    )
```
This method has two required arguments, `jdbc_table` (the JDBC table to fetch from) and `snowflake_table` (the Snowflake table to fetch from).
There are optional arguments that can be passed in: `snowflake_database`, `snowflake_schema`, and `jdbc_database`.
If any one of these arguments is passed in directly, `hdv` will use the passed in argument instead of the default configured
in `hdv_profiles.yml`. This method uses `hdv_profiles.yml` and the `.yml` must be configured before running this method.

#### `hdv` called via command line
`hdv -sf <snowflake_table> -jdbc <jdbc_table>`

#### Parameters
Both of the following parameters are required:
- `[-sf] [--snowflake_table] <snowflake_table>:
Snowflake table to run validation on. Can be called with [-sf] or [--snowflake_table]`
- `[-jdbc] [--jdbc_table] <jdbc_table>:
  JDBC table to run validation on. Can be called with [-jdbc] or [--jdbc_table]`
  
### Examples
Example: `.hashmap_data_validator/hdv_profiles.yml`
```yaml
source:
  jdbc:
    host: my_jdbc_host              # jdbc:mysql://localhost
    port: my_jdbc_port              # 3306
    database: my_jdbc_database
    user: jdbc_username
    password: jdbc_password
    jar_file: my_jar_file_path      # Example: Users/user/mysql-connector-java-8.0.23/mysql-connector-java-8.0.23.jar
    driver: my_driver_name          # Example: com.mysql.cj.jdbc.Driver
sink:
  snowflake:
    username: my_snowflake_username
    password: my_snowflake_password
    account: my_snowflake_account
    database: my_snowflake_database
    schema: my_snowflake_schema
    role: my_snowflake_role
    warehouse: my_snowflake_warehouse
```

`hdv` called inside a python file as a method:
```python
from hdv import hdv

hdv(snowflake_table='my_snowflake_table', jdbc_table='my_jdbc_table')
```

`hdv` called via the command line:

1. `hdv -sf my_snowflake_table -jdbc my_jdbc_table`
2. `hdv --snowflake_table my_snowflake_table --jdbc_table my_jdbc_table`
