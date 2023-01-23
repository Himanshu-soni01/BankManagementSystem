import sqlite3

conn=sqlite3.connect('BMS.db')

cur=conn.cursor()

cur.execute("CREATE TABLE account(Name TEXT ,AccNo INT NOT NULL UNIQUE CHECK(AccNo>100),Password INT NOT NULL,Contact INT NOT NULL,DOB ,Address TEXT,OpeningBalance INT CHECK(OpeningBalance>=0))")

cur.execute("CREATE TABLE amount(AccNo NOT NULL,Password INT NOT NULL CHECK(Password>=1001), Balance CHECK(BALANCE>=0))")

# data1=[('Himanshu Soni',1001,1234,1234567892,'20.10.2000','Sojat',100)]

# data2=[(1001,1234,100)]

# cur.executemany('insert into account values(?,?,?,?,?,?,?)',data1)

# cur.executemany('insert into amount values(?,?,?)',data2)

conn.commit()