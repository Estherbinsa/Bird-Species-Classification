import pymysql
conn=pymysql.connect(host='localhost',user='root',password='',database='bird')

def logindata(qry):
    cursor=conn.cursor()
    qry=qry
    cursor.execute(qry)
    data=cursor.fetchone()
    #data=cursor
    return data

def selectdata(qry):
    cursor=conn.cursor()
    cursor.execute(qry)
    data=cursor.fetchone()
    #data=cursor
    return data

def insertdata(qry):        
    cursor=conn.cursor()
    
    cursor.execute(qry)
    conn.commit()

def selectalldata(qry):
    cursor=conn.cursor()
   
    cursor.execute(qry)
    #data=cursor.fetchone()
    data=cursor
    return data

def deletedata(qry):        
    cursor=conn.cursor()
    sql=qry
    cursor.execute(sql)
    conn.commit()
