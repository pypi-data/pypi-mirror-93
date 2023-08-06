# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2020, 2021
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import datetime
import json
import os
import unittest
from ibm_wos_utils.joblib.utils.db_utils import DbUtils, JDBCUtils
from ibm_wos_utils.joblib.exceptions.client_errors import *

from pyspark.sql import SparkSession, SQLContext
sparkApp = SparkSession\
        .builder\
        .appName("TestDbUtils")
spark = sparkApp.getOrCreate()

class TestDbUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_read_data_from_db2(self):
        # Enter database details
        database_name = ""
        table_name = ""
        schema_name = ""
        user = ""
        password = ""
        jdbc_url = "jdbc:db2://<host>:<port>/<database_name>"
        driver = "com.ibm.db2.jcc.DB2Driver"

        # Read certificate from file
        file_path = os.path.abspath(os.getcwd()) + "/ibm_wos_utils/joblib/tests/ssl_cert.txt"
        with open(file_path,"r") as f:
            ssl_certificate = f.read()
        
        connection_properties = DbUtils.get_connection_properties(user, password, jdbc_url, driver, ssl_certificate)
        try:
            df = DbUtils.get_table_as_dataframe(spark,
                                                "jdbc",
                                                database_name,
                                                table_name,
                                                schema_name=schema_name,
                                                connection_properties=connection_properties
                                                )
            row_count = df.count()
            assert df is not None and row_count > 0
        except Exception as e:
            assert False, "Failed to read data from DB2 using JDBC. Error: {}".format(str(e))
        finally:
            # Delete certificate file in case of SSL
            DbUtils.delete_certificate_file(connection_properties)
    
    def test_read_data_from_db2_with_timestamp(self):
        # Enter database details
        database_name = ""
        table_name = ""
        schema_name = ""
        user = ""
        password = ""
        jdbc_url = "jdbc:db2://<host>:<port>/<database_name>"
        record_timestamp_column = "scoring_timestamp"

        connection_properties = DbUtils.get_connection_properties(user, password, jdbc_url)
        df = DbUtils.get_table_as_dataframe(spark,
                                            "jdbc",
                                            database_name,
                                            table_name,
                                            schema_name=schema_name,
                                            connection_properties=connection_properties,
                                            record_timestamp_column=record_timestamp_column,
                                            start_time=str(datetime.datetime.utcnow().isoformat() + 'Z')
                                            )
        # The start date is current time, so it should return empty dataframe
        assert df is not None
        assert df.count() == 0
    
        df = DbUtils.get_table_as_dataframe(spark,
                                            "jdbc",
                                            database_name,
                                            table_name,
                                            schema_name=schema_name,
                                            connection_properties=connection_properties,
                                            record_timestamp_column=record_timestamp_column,
                                            end_time="2020-01-21T00:00:00.00Z"
                                            )
        # The end date is earlier than table creation time, so it should return empty dataframe
        assert df is not None
        assert df.count() == 0

    def test_read_data_from_db2_invalid_driver(self):
        # Enter database details
        database_name = ""
        table_name = ""
        schema_name = ""
        user = ""
        password = ""
        jdbc_url = "jdbc:db2://<host>:<port>/<database_name>"
        driver = "test_driver"

        connection_properties = DbUtils.get_connection_properties(user, password, jdbc_url, driver)
        try:
            df = DbUtils.get_table_as_dataframe(spark,
                                                "jdbc",
                                                database_name,
                                                table_name,
                                                schema_name=schema_name,
                                                connection_properties=connection_properties
                                                )
        except DatabaseError as clerr:
            assert "Specified JDBC driver '{}' could not be found".format(driver) in str(clerr)

if __name__ == '__main__':
    unittest.main()
