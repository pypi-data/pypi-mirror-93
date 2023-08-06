# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2020, 2021
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import base64
import tempfile
import logging
import os
import re
import ssl
from datetime import datetime

import pyspark.sql.functions as F
from ibm_wos_utils.joblib.utils.constants import *
from ibm_wos_utils.joblib.exceptions.client_errors import *
from ibm_wos_utils.joblib.utils import hive_utils

logger = logging.getLogger(__name__)


class DbUtils:
    """
    Utility class for database interaction
    """

    @classmethod
    def get_table_as_dataframe(
            cls,
            spark,
            storage_type: str,
            database_name: str,
            table_name: str,
            schema_name: str = None,
            connection_properties: dict = None,
            sql_query: str = None,
            columns_to_map: list = [],
            columns_to_filter: list = [],
            record_timestamp_column: str = None,
            start_time: str = None,
            end_time: str = None):

        """Get database table as dataframe.

        Additionally, it does:
        - Converts any column of boolean type to string type
        - Filter out header row based on columns_to_filter. Only uses the first column found in the table.
        - If provided, fetches records based on the timestamps

        It does NOT do any validation.

        Arguments:
            spark {SparkSession} -- Spark Session to use
            database_name {str} -- Name of Database
            table_name {str} -- Name of table in the database

        Keyword Arguments:
            schema_name {str} -- Name of schema
            connection_properties {dict} -- Dictionary of JDBC connection details like url, user, password, driver
            sql_query {str} -- SQL query
            columns_to_map {list} -- List of columns to map from lowercase to correct case
            columns_to_filter {list} -- List of columns to filter out header row. Uses the first column found in table (default: {[]})
            record_timestamp_column {str} -- Name of the column with modeling role record-timestamp (default: {None})
            start_time {str} -- Start Time in ISO format `%Y-%m-%dT%H:%M:%S.%f` (default: {None})
            end_time {str} -- End Time in ISO format `%Y-%m-%dT%H:%M:%S.%f` (default: {None})

        Returns:
            pyspark Dataframe

        """

        if storage_type == StorageType.HIVE.value:
            spark_df = hive_utils.get_table_as_dataframe(spark,
                                                         database_name,
                                                         table_name,
                                                         columns_to_map,
                                                         columns_to_filter=columns_to_filter,
                                                         record_timestamp_column=record_timestamp_column,
                                                         start_time=start_time,
                                                         end_time=end_time)
            return spark_df
        elif storage_type == StorageType.JDBC.value:
            spark_df = JDBCUtils.get_table_as_dataframe(spark,
                                                        database_name,
                                                        table_name,
                                                        schema_name,
                                                        connection_properties,
                                                        sql_query=sql_query
                                                        )
        else:
            raise Exception(
                "Unsupported storage type: {}. Only supported storage connections are {}.".format(storage_type, [
                    StorageType.HIVE.value, StorageType.JDBC.value]))

        logger.info(spark_df.printSchema())
        logger.info("******* Number of Partitions: {} ********".format(spark_df.rdd.getNumPartitions()))
        
        # Convert boolean columns to string
        spark_df_dtypes = dict(spark_df.dtypes)
        logger.info(spark_df_dtypes)
        for col in spark_df.columns:
            if spark_df_dtypes[col] == "boolean":
                spark_df = spark_df.withColumn(col, spark_df[col].cast("string"))
                logger.info(" - Changed column {} of type boolean to type string.".format(col))

        if record_timestamp_column is not None and record_timestamp_column in spark_df.columns:
            # assumptions: start_time and end_time are in isoformat
            # %Y-%m-%dT%H:%M:%S.%fZ
            if start_time is not None:
                start_time = datetime.strptime(start_time, TIMESTAMP_FORMAT)
                spark_df = spark_df.where(
                    F.col(record_timestamp_column) >= start_time)

            if end_time is not None:
                end_time = datetime.strptime(end_time, TIMESTAMP_FORMAT)
                spark_df = spark_df.where(
                    F.col(record_timestamp_column) <= end_time)

        logger.info(spark_df.explain())
        logger.info(spark_df.printSchema())
        return spark_df

    @classmethod
    def get_connection_properties(
            cls,
            user: str,
            password: str,
            url: str,
            driver: str = None,
            ssl_certificate = None):
        
        """
        Construct dictionary of connection parameters
        Arguments:
            user {str} -- Username
            password {str} -- Password
            url {str} -- JDBC URL

        Keyword Arguments:
            driver {str} -- Name of the JDBC driver
            ssl_certificate -- The SSL certificate
        """
        
        connection_properties = dict()
        connection_properties["user"] = user
        connection_properties["password"] = password
        connection_properties["url"] = url
        if driver is not None:
            connection_properties["driver"] = driver
        if ssl_certificate is not None:
            connection_properties["sslConnection"] = "true"
            # Add location of certificate file
            connection_properties["ssl_certificate"] = ssl_certificate
            f = cls.create_certificate_file(connection_properties)
            connection_properties["sslCertLocation"] = f
        # Add connection timeout
        connection_properties["connectionTimeout"] = str(DEFAULT_CONNECTION_TIMEOUT)

        return connection_properties

    @classmethod
    def create_certificate_file(cls, connection_properties):
        certificate_base64 = connection_properties.get("ssl_certificate")
        certificate = None
        cert_file = None
        if certificate_base64:
            # if certificate already set in the connection_details
            if 'BEGIN CERTIFICATE' not in certificate_base64:
                # If 'BEGIN CERTIFICATE' is not present, assuming that it will be a base64 encoded.
                certificate = base64.b64decode(
                    certificate_base64.strip()).decode()
            else:
                certificate = certificate_base64.strip()
            del connection_properties["ssl_certificate"]
        else:
            # else get it from the host
            certificate = cls.get_certificate_from_host(connection_properties.get("url"))
            
        with tempfile.NamedTemporaryFile(mode="w", prefix="db2ssl_", suffix="_cert.arm", delete=False) as f:
            cert_file = f.name
            f.write(certificate)
        return cert_file

    @classmethod
    def get_certificate_from_host(cls, url):
        host = None
        port = None
        certificate = None
        host_str = re.search("//(.*)/", url)
        if host_str:
            host_str = host_str.group(1)
            if ":" in host_str:
                arr = host_str.split(":")
                host = arr[0]
                port = arr[1]
        certificate = ssl.get_server_certificate(
            (host, port))
        return certificate
    
    @classmethod
    def delete_certificate_file(cls, connection_properties):
        cert_file = connection_properties.get("sslCertLocation")
        if cert_file is not None and (os.path.isfile(cert_file)):
            try:
                os.remove(cert_file)
                logger.info('Deleted certificate file {}'.format(cert_file))
            except:
                logger.warning(
                    "Failed to delete cert file " + cert_file + ".")


class JDBCUtils:
    """
    Utility class for database interaction using JDBC
    """

    @classmethod
    def get_table_as_dataframe(
            cls,
            spark,
            database_name: str,
            table_name: str,
            schema_name: str,
            connection_properties: dict,
            sql_query: str = None):
        
        """
        Get database table as dataframe using JDBC
        Arguments:
            spark {SparkSession} -- Spark Session to use
            database_name {str} -- Name of Database
            table_name {str} -- Name of table in the database
            schema_name {str} -- Schema name
            connection_properties {dict} -- Dictionary of JDBC connection details like url, user, password, driver

        Keyword Arguments:
            sql_query {str} -- SQL query
        """
        
        if sql_query is None:
            sql_query = "(select * from {}.{})".format(schema_name, table_name)
        if not (sql_query.startswith("(") and sql_query.endswith(")")):
            sql_query = "({})".format(sql_query)
        url = connection_properties.get("url")
        try:
            spark_df = spark.read \
                .jdbc(url, sql_query , properties=connection_properties)

        except Exception as e:
            error_message = "Error while reading from database with JDBC. Error: {}".format(str(e))
            # If specified driver does not exist, raise error with proper message.
            if "java.lang.ClassNotFoundException" in str(e):
                driver = connection_properties.get("driver")
                error_message = "Specified JDBC driver '{}' could not be found.".format(driver)
            raise DatabaseError(error_message)

        return spark_df

    