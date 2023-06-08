from flask import Flask, render_template
import pymysql

app = Flask(__name__)

# Configure MySQL connection
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="try"
)

@app.route("/")
def display_table():
    # Retrieve data from the table
    cursor = conn.cursor()
    sql = "SELECT * FROM history"
    cursor.execute(sql)
    result = cursor.fetchall()

    if len(result) > 0:
        # Render the template with the retrieved data
        return render_template("table.html", data=result)
    else:
        return "No records found."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
