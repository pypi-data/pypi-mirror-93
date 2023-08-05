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

    def hdv(self, jdbc_table: str, snowflake_table: str, snowflake_database: str = None,
            snowflake_schema: str = None, jdbc_database: str = None):
        """validation method: runs expectations on row count and row hash values between Snowflake and JDBC tables"""

        try:
            # get jdbc pandas dataframe
            self.initialize_jdbc(database=jdbc_database,
                                 table=jdbc_table
                                 )

            # get snowflake pandas dataframe
            self.initialize_snowflake(database=snowflake_database,
                                      schema=snowflake_schema,
                                      table=snowflake_table
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
            webbrowser.open('file://' + os.path.realpath('expectation_report.html'))

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
        html_str = j2h.convert(json=self.json_str)

        # write html string to file
        with open(os.path.realpath('expectation_report.html'), "w") as html_report:
            html_report.write(html_str)
            html_report.close()
        return
