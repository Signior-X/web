from mysqlconnect import mydb, mycursor, sqlerror

# If you want to change the schema, then remove the table from the server first!

try:
    t1 = "CREATE TABLE Todo(id int(3) primary key auto_increment, title varchar(64) not null, about varchar(1000), date date);"
    mycursor.execute(t1)
    print("successfully created Table Todo")
except sqlerror as err:
    print(err)

try:
    t2 = "CREATE Table loginDetails(username varchar(64) primary key, password varchar(300));"
    mycursor.execute(t2)
    print("successfully created table loginDetails")
except sqlerror as err:
    print(err)
