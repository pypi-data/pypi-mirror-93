import great_expectations as ge
import pandas as pd
from json2html import Json2Html
import webbrowser
import os
from hdv.jdbc_objects.jdbc_object import JDBCObject
from hdv.snowflake_objects.snowflake_object import SnowflakeObject


class Validator(SnowflakeObject, JDBCObject):
    """Class that holds the validate method"""

    # row count validation
    row_count_valid = False
    # row hash validation
    row_hash_valid = False
    # great expectations snowflake dataframe
    ge_sf_df = None
    # hash df
    hash_df = None
    # json string to generate html report
    json_str = str

    def hdv(self, jdbc_table: str = None, snowflake_table: str = None, snowflake_database: str = None,
            snowflake_schema: str = None, jdbc_database: str = None, sf_query: str = None, jdbc_query: str = None):
        """validation method: runs expectations on row count and row hash values between Snowflake and JDBC tables"""

        try:
            # get jdbc pandas dataframe
            self.initialize_jdbc(database=jdbc_database,
                                 table=jdbc_table,
                                 sql_query=jdbc_query
                                 )

            # get snowflake pandas dataframe
            self.initialize_snowflake(database=snowflake_database,
                                      schema=snowflake_schema,
                                      table=snowflake_table,
                                      sql_query=sf_query
                                      )

            # run row count expectation on dataframes
            self.count_df_rows()

            # run row hash comparison expectation on dataframes
            self.compare_row_hashes()

            # create a json string from validation results
            self.json_str = '{"row_count_expectation": ' + self.row_count_valid + ', "row_hash_expectation": ' + self.row_hash_valid + "}"

            # generate html report from json string (.html file gets created from directory where the method is run)
            self.generate_html_report()

            # open the .html report
            webbrowser.open('file://' + os.path.realpath('validation_report.html'))

        except Exception as e:
            self._logger.error(e)
            return False

        finally:
            # close connections
            if self.jdbc_connection:
                self.jdbc_connection.close()
            if self.sf_connection:
                self.sf_connection.close()
            if self.sf_cursor:
                self.sf_cursor.close()

    def generate_hash_list(self, df: pd.DataFrame):
        """generates a list of hash tuples over the rows in a dataframe"""
        hash_list = df.apply(lambda x: hash(tuple(x)), axis=1).tolist()

        return hash_list

    def count_df_rows(self):
        """expectation to count dataframe rows"""

        # create a great expectations dataframe from the snowflake dataframe for row count expectation
        self.ge_sf_df = ge.from_pandas(self.sf_df)

        # run row count expectation
        self.row_count_valid = str(self.ge_sf_df.expect_table_row_count_to_equal(len(self.jdbc_df.index)))

    def compare_row_hashes(self):
        """expectation to compare row hash strings"""

        # construct series from snowflake hash list
        sf_series = pd.Series(self.generate_hash_list(self.sf_df), name='sf_hashes')

        # construct series from jdbc hash list
        jdbc_series = pd.Series(self.generate_hash_list(self.jdbc_df), name='jdbc_hashes')

        # create the hash dataframe to be used in the hash expectation through concatenation
        self.hash_df = pd.concat([sf_series, jdbc_series], axis=1)

        # convert pandas dataframe to a great expectations dataframe
        self.hash_df = ge.from_pandas(self.hash_df)

        # run hash comparison expectation
        self.row_hash_valid = str(self.hash_df.expect_column_pair_values_to_be_equal(column_A='sf_hashes',
                                                                                     column_B='jdbc_hashes',
                                                                                     ignore_row_if="either_value_is_missing"))

    def generate_html_report(self):
        """converts json string to html and writes to html file"""

        # initiate json2html object
        j2h = Json2Html()

        # convert json to html
        table_str = j2h.convert(json=self.json_str, table_attributes="class=\"table table-bordered table-hover\"")

        # insert table string into html string
        html_str = f'<!doctype html><html lang="en"><head><!-- Required meta tags --><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><!-- Bootstrap CSS -->' \
                    '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"><title>Hashmap-Data-Validator</title></head>' \
                    '<header class="navbar navbar-expand-lg navbar-dark bg-dark"><div class="collapse navbar-collapse"><div class="mx-auto my-2 text-white"><h3>Hashmap Data Validator</h3></div></div></header>' \
                    f'<body>{table_str}<!-- Optional JavaScript --><!-- jQuery first, then Popper.js, then Bootstrap JS -->' \
                    f'<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>' \
                    f'<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>' \
                    f'<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>' \
                    f'</body></html>'

        # write html string to file
        with open(os.path.realpath('validation_report.html'), "w") as html_report:
            html_report.write(html_str)
            html_report.close()
        return
