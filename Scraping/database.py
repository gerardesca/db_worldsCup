import mysql.connector as mysql
from mysql.connector import Error
import csv

try:
    db = mysql.connect(
        host="localhost",
        user="db_ball_user",
        passwd="D@t@Ball10",
        database="db_databall"
    )
    if db.is_connected():
        print("Successful connection")
        cursor = db.cursor()
        
        #Drop Tables If Exists
        cursor.execute("DROP TABLE IF EXISTS tbl_editions")
        
        #Create Tables
        create_editions ='''CREATE TABLE tbl_editions(
            rowid INT AUTO_INCREMENT PRIMARY KEY,
            fk_edition CHAR(50) NOT NULL,
            fk_group CHAR(50),
            fk_team CHAR(100)
        )'''
        cursor.execute(create_editions)
        #Insert Values
        insert_editions = "INSERT INTO tbl_editions (fk_edition, fk_group, fk_team) VALUES (%s, %s, %s)"
        with open('editions.csv', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                #print(row)
        #value = ('1930','Group 1','Argentina')
                cursor.execute(insert_editions, row)
                db.commit()
except Error as ex:
    print("Error during connection: ", ex)
""" finally:
    if db.is_connected():
        db.close()
        print("The connection has ended") """
        


