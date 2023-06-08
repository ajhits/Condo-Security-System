import mysql.connector
import json


host = "localhost"
user = "root"
password = ""
database = "smart_ai_home_security"

# Connection to the database
# data = mysql.connector.connect(host=host, user=user, password=password, database=database)
# cursor = data.cursor()  


# Connection query to the database
def connection():
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        result = cursor.fetchone()
        print(result)

        return conn

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

    
# def __connectionCheck():

#     try:

#     # Test connection
#         cursor.execute("SELECT VERSION()")
#         result = cursor.fetchone()

#         if result:
#             print("connected to database")
#             print("MySQL Server version:", result[0])
#         else:
#             print("Connection failed!")

#         # Closing the connection
#         # cursor.close()
#         # data.close()
        
#         return cursor

#     except mysql.connector.Error as error:
#         print("Error while connecting to MySQL:", error)


# __connection()


# create data in History table
def createHistory(images=None, name=None, time_in=None, date=None):
    result = ""
    try:
        conn = connection()
        cursor = conn.cursor()
        
        # Create the HISTORY table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS HISTORY (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            Images LONGTEXT,
            Name VARCHAR(255),
            TimeIn VARCHAR(255),
            Date VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Insert data into the HISTORY table
        insert_query = """
        INSERT INTO HISTORY (person, name, time, date)
        VALUES (%s, %s, %s, %s)
        """
        query = (images, name, time_in, date)
        cursor.execute(insert_query, query)
        conn.commit()

        print("Data inserted successfully!")
        result = "Data inserted successfully!"

    except mysql.connector.Error as err:
        print("Error:", err)
        result = str(err)

    # Close the cursor and connection
    cursor.close()
    conn.close()
    
    return result

# Read data from History table
def readHistory():
    try:
        conn = connection()
        cursor = conn.cursor()

        # Select all rows from the HISTORY table
        select_query = "SELECT * FROM HISTORY"
        cursor.execute(select_query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Convert rows to array
        data_list = []
        for row in rows:
            row_array = list(row)
            data_list.append(row_array)

        # Convert array to JSON
        data_json = json.dumps(data_list)

        cursor.close()
        conn.close()

        # Return the JSON response
        return data_list

    except mysql.connector.Error as err:
        print("Error:", err)
        return None



# # update data in History table
def updateHistory(ID=None,Images=None, new_name=None, new_time_in=None, new_date=None):
    try:
        conn = connection()
        cursor = conn.cursor()

        # Update the specified record in the HISTORY table
        update_query = "UPDATE HISTORY SET person = %s, name = %s, time = %s, date = %s WHERE ID = %s"
        query = (Images,new_name, new_time_in, new_date, ID)
        cursor.execute(update_query, query)
        conn.commit()

        if cursor.rowcount > 0:
            print("Data updated successfully!")
        else:
            print("No matching record found.")

    except mysql.connector.Error as err:
        print("Error:", err)

    # Close the cursor and connection
    cursor.close()
    conn.close()


# delete data in History table
def deleteHistory(ID):
    
    try:

        conn = connection()
        cursor = conn.cursor()

        # Delete the specified record from the HISTORY table
        delete_query = "DELETE FROM HISTORY WHERE ID = %s"
        query = (ID,)
        cursor.execute(delete_query, query)
        conn.commit()

        if cursor.rowcount > 0:
            print("Data deleted successfully!")
        else:
            print("No matching record found.")

    except mysql.connector.Error as err:
        print("Error:", err)

    # Close the cursor and connection
    cursor.close()
    conn.close()


# createHistory(
#     images="Hello Friend",
#     name="Elliot Alderson",
#     time_in="3:00pm",
#     date="June 8 2023"
# )

# history_data= readHistory()
# print(history_data)


# updateHistory(
#     ID=3,
#     Images="chek ssscheck",
#     new_name="Art Lisboa",
#     new_date="june 24 2023",
#     new_time_in="6:30"
# )

# deleteHistory(7)

