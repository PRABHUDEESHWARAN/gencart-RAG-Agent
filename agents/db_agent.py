from langchain.agents import tool
import pymysql
import logging
import sys
import traceback
import re

def clean_sql_command(sql_command):
    sql_command=sql_command.strip()
    sql_command=re.sub(r'[;].*$',';',sql_command)
    if not sql_command.endswith(';'):
        sql_command+=';'

    return sql_command

@tool
def queryDB(sql_query:str):
    """
    This tool is designed to retrieve information from a MySQL Database. It should ONLY be used when the question 
    is directly related to the details of the store and its data, such as product availability, category, color, 
    or description.

    Example questions this tool can handle:
        - Is a blue pen available?
        - Are gel pens available?
        - What is the price of gel pens in general?
        - What is the price of blue gel pens?
        
    IMPORTANT INSTRUCTIONS FOR THE LLM:
    - Always query the database for the available categories first using: "SELECT DISTINCT CATEGORY FROM PRODUCT;"
    - Normalize the user's input (e.g., lowercase) and compare it with the retrieved categories to ensure the category exists.
    - If the category exists, proceed to query for the specific product using the provided attributes (CATEGORY, COLOUR, DESCRIPTION).
    - If the category does not exist, inform the user that the category is not available in the database.

    HERE IS THE SCHEMA OF THE TABLES PRESENT IN THE DATABASE:

    Table Name: PRODUCT
    Description: Stores information about the products available in the store.
    Columns:
        - ID (INTEGER, PRIMARY KEY): Unique Identifier for the product.
        - CATEGORY (TEXT): Describes the category of the product.
        - COLOUR (TEXT): Color of the product.
        - DESCRIPTION (TEXT): Description of the product in detail.

    USE ONLY THE ABOVE ATTRIBUTES TO QUERY THE TABLE.

    Args:
        sql_query (str): A SQL query string to search the database.

    Returns:
        str: A message indicating the result of the query.
    
    """

    mysql_server_name="localhost"
    database_name="domaindb"
    sql_query=clean_sql_command(sql_query)
    try:
        logging.info(f"Connecting to MySQL db: '{database_name} on server '{mysql_server_name}'")
        mydb=pymysql.connect(
            host=mysql_server_name,
            port=3306,
            user='root',
            password='admin@123',
            database=database_name,
            connect_timeout=5
        )
        logging.info("successfully connected to Mysql DB")
    except pymysql.MySQLError as e:
        logging.error(f"mysql err : {e}")
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        logging.error(f"unexpected err: {e}")
        traceback.print_exc()
        sys.exit(1)

    try:
        mycursor=mydb.cursor()
        logging.info("cursor created")
    except pymysql.MySQLError as e:
        logging.error(f"mysql err : {e}")
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        logging.error(f"unexpected err: {e}")
        traceback.print_exc()
        sys.exit(1)

    finally:
        try:
            mycursor.execute(sql_query)
            records=mycursor.fetchall()
            mycursor.close()
            logging.info("connection closed")
            return str(records)
        except Exception as e:
            logging.error(f"error in inference: {e}")
    
   