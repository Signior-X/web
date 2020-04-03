from mysqlconnect import mydb, mycursor

t1 = "CREATE TABLE Todo(id int(3) primary key auto_increment, title varchar(64) not null, about varchar(1000), date date);"
#mycursor.execute("use webdb")
mycursor.execute(t1)
print("successfully created Table Todo")
