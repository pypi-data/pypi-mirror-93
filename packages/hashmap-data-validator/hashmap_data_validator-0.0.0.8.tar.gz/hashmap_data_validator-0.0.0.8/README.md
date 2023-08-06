# Hashmap Data Validator

## MVP
This repo holds the hashmap-data-validator. Hashmap-data-validator is a tool used for data validation between a JDBC connectable database and a Snowflake database.

## How it works
HDV uses great expectations to run validation on the two tables. It supports connections to Snowflake tables with the Snowflake-connector-python and to JDBC tables with Jaydebeapi. 
It currently runs expectations on row count and row hash values to validate the tables. The main `hdv` method can be found in `validator.py`. It is imported inside `__init__.py` and therefore
the user can import the method in their own project. The row count expectation runs an expectation on the Snowflake table row count against the JDBC table row count. 
To run the row hash expectation, HDV generates row hash values for every row in both tables. These row hash values are saved as a pandas series, then are put into a pandas 
dataframe as column. The row hash expectation is run on the dataframe with the two row hash columns by comparing the values in each column row by row.

The `hdv` command line method is configured in `cli_validator.py`. It uses the python `Click` library with `setuptools` to be callable via the CLI.
## How to use
* The user installs the package via PyPi with ```pip install hashmap-data-validator```
* After installation, user needs to run a `.py` file with the following import: `from hdv import hdv`
* A `.yml` file will then be created in the user's `home` directory with the following path: `.hashmap_data_validator/hdv_profiles.yml`
* The user then configures their JDBC and Snowflake credentials in the `.yml`. HDV uses this file to manage the JDBC and Snowflake connections for the user.
* After configuration is complete, the user can call `hdv` two different ways:
    1. From the command line
    2. From a python file as an imported method
  
* HDV writes the validation results to a newly created `validation_results.html` file (if it does not exist) in the directory where the command is called and opens that file in your browser
    
## API
## `hdv` called via imported python method
```python
hdv(
    jdbc_table: str = None, 
    snowflake_table: str = None, 
    snowflake_database: str = None,
    snowflake_schema: str = None, 
    jdbc_database: str = None,
    sf_query: str = None,
    jdbc_query: str = None
    )
```
There are two different ways to use this method:
1. Pass in values for the `jdbc_table` (the JDBC table to fetch from) and `snowflake_table` (the Snowflake table to fetch from) arguments. If you pass in values for those two arguments, `hdv` will 
run a default sql query over both passed in tables `select * from ...` and will run validation over all columns and rows in those tables.
   
2. Pass in SQL queries for both your JDBC and Snowflake tables by using the `sf_query` and `jdbc_query` arguments. Passing in your own SQL queries allows you to choose the scope of what gets validated in your tables. Please note that 
the queries you pass in for your Snowflake and JDBC tables must yield the same table results. Otherwise, the validation will always fail.

There are optional arguments that can be passed in: `snowflake_database`, `snowflake_schema`, and `jdbc_database`.
If any one of these arguments is passed in directly, `hdv` will use the passed in argument instead of the default configured
in `hdv_profiles.yml`. This method uses `hdv_profiles.yml` and the connection credentials for both Snowflake and JDBC in the `.yml` must be configured before running this method.

## `hdv` called via command line
There are two different ways to use this method via the command line:
### 1. `hdv -sf <snowflake_table> -jdbc <jdbc_table>`
   #### Parameters
Both of the following parameters are required for the first option:
- `[-sf] [--snowflake_table] <snowflake_table>`: Snowflake table to run validation on. Can be called with [-sf] or[--snowflake_table]
- `[-jdbc] [--jdbc_table] <jdbc_table>`: JDBC table to run validation on. Can be called with [-jdbc] or [--jdbc_table]
  
### 2. `hdv --jdbc_sql '<your jdbc sql query>' --sf_sql '<your snowflake sql query>'`
#### Parameters
Both of the following parameters are required for the second option:
- `[--jdbc_sql] '<your jdbc sql query>'`: SQL query to be run in your JDBC environment. Pass in the SQL query as a string where `''` quotations encompass the query.
- `[--sf_sql] '<your snowflake sql query>'`: SQL query to be run in your Snowflake environment. Pass in the SQL query as a string where `''` quotations encompass the query.
  
## Examples
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

### `hdv` called inside a python file as a method using the table arguments:
```python
from hdv import hdv

hdv(snowflake_table='my_snowflake_table', jdbc_table='my_jdbc_table')
```
This will `select * from my_snowflake_database.my_snowflake_schema.my_snowflake_table` and 
`select * from my_jdbc_database.my_jdbc_table`. The validation will then be run on the resulting dataframes.


### `hdv` called inside a python file as a method using passed in sql queries:
```python
from hdv import hdv

snowflake_query = 'select col_1, col_2 from database.schema.table LIMIT 100000'
jdbc_query = 'select col_1, col_2 from database.table LIMIT 100000'

hdv(sf_query=snowflake_query, jdbc_table=jdbc_query)
```
The above method call does not use the databases or schemas configured in the `.yml` file. HDV manages your Snowflake and JDBC database connections
for you, but runs your SQL query instead of the default `select * from...` and runs validation on the resulting
dataframes.

### `hdv` called via the command line using the table arguments:

- `hdv -sf my_snowflake_table -jdbc my_jdbc_table`
- `hdv --snowflake_table my_snowflake_table --jdbc_table my_jdbc_table`

### `hdv` called via the command line using SQL query arguments:

- `hdv --jdbc_sql 'select col_1, col_2 from database.table LIMIT 100000' --sf_sql 'select col_1, col_2 from database.schema.table LIMIT 100000'`

