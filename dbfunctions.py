import pymysql
import datetime


# In[48]:

#This creates a connection to the database
def makeConnection():
    host = "datasparkdb.cbbvbxlm9nap.us-east-1.rds.amazonaws.com"
    port = 3306
    dbname = "DataSparkDataBase"
    user = "aarasu"
    password = "aabbccdd1234"
    conn = openMySqlConnection(host, port, dbname, user, password)
    return conn

# Connects to the database.
def openMySqlConnection(host, port, dbname, user, password):
    conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
    print("The connection is open")
    return conn

#Disconnect DB
def closeMySqlConnection(conn):
    conn.close()
    print("The connection is closed")

# Creating a new user in the Tableau Database and granting them basic privileges to view present tables.
def createUser(userName, userPass, tablenames):
    try:
        conn = makeConnection()
        stmntNewUser = "CREATE USER IF NOT EXISTS '" + userName + "'@'%'" + " IDENTIFIED BY '" + userPass + "';"
        with conn.cursor() as cursor:
            sql = stmntNewUser
            cursor.execute(sql)
            
        for i in range(len(tablenames)):
            with conn.cursor() as cursor:
                stmntNewUser = "Grant SELECT on DataSparkDataBase."+tablenames[i]+" TO '"+userName+"'@'%' ;"
                cursor.execute(stmntNewUser)
        
    finally:
        closeMySqlConnection(conn)



# Creating a user specified view
def createView(tablenames, columnNames, viewName, userName, databaseName):
    now = datetime.datetime.now()
    #Adding time of view creation to the view name to reduce the probability that 2 users have the same view name
    a = "_"+str(now.day)+"_"+str(now.month)+"_"+str(now.year)+"_"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second)
    
    try:
        conn = makeConnection()
        conn1 = makeConnection()
        #The Following Creates  the view statement user has requested
        stmt = "Create view " + viewName + a + " as"
        selectstmt = " select " + tablenames[0]+".POA_CODE_2016, "
        counter=0
        for i in columnNames:
            if(i!="POA_CODE_2016"):
                selectstmt += i + ", "
                counter+=1
        selectstmt=selectstmt[:-2]
        selectstmt+= " from "
        
        for i in tablenames:
            selectstmt+= i + ", "
        selectstmt=selectstmt[:-2]
        if(len(tablenames)>1):
            selectstmt+= " where "
            for j in range(len(tablenames)-1):
                selectstmt+= tablenames[0]+".POA_CODE_2016 = " + tablenames[j+1] + ".POA_CODE_2016 AND "
            selectstmt=selectstmt[:-4]
        stmt= stmt + selectstmt
        pvtstmt = ''
        #Creating the pivoted view using union all command as MYSQL doesn't have the Pivot funciton inbuilt
        print('check2')
        print(stmt)
        print(counter)
        for i in range(len(columnNames)):
            if(columnNames[i]!= "POA_CODE_2016"):
                pvtstmt = pvtstmt+ 'SELECT POA_CODE_2016, \''+columnNames[i]+'\' Attributes, '+columnNames[i]+' val from ('+selectstmt+') p union all '
        pvtstmt=pvtstmt[:-11]
        pvtstmt = "Create view pivoted_"+ viewName + a + " as " + pvtstmt
        print('check1')
        print(pvtstmt)
        
        with conn.cursor() as cursor:
            cursor.execute(stmt)
            cursor.execute(pvtstmt)
        # Granting permissions to both the views created
        grantPermissions(databaseName, viewName+a, userName)
        grantPermissions(databaseName, 'pivoted_'+viewName+a, userName)
    finally:
        closeMySqlConnection(conn)
        

#Gives permissions in a specif view
def grantPermissions(databaseName, viewName, userName):
    stmnt = "GRANT ALL ON " + databaseName + "." + viewName + " TO '" + userName + "'@'%';"
    try:
        conn = makeConnection()
        with conn.cursor() as cursor:
            sql = stmnt
            cursor.execute(sql)
    finally:
        closeMySqlConnection(conn)



# Checks if user id exists
def checkUser(username):
    try:
        conn = makeConnection()
        stmntNewUser = "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '"+username+"')"

        with conn.cursor() as cursor:
            sql = stmntNewUser
            #print(sql)
            cursor.execute(sql)
            viewNames = [i[0] for i in cursor.fetchall()]

    finally:
        closeMySqlConnection(conn)
        return viewNames[0]



#This function revokes permissions of a user
def revokePermissions(userName):
    stmnt = "REVOKE ALL PRIVILEGES ON *.* FROM '" + userName + "'@'%';"
    try:
        conn = makeConnection()
        with conn.cursor() as cursor:
            sql = stmnt
            cursor.execute(sql)
    finally:
        closeMySqlConnection(conn)

#This function will 
def getTableNames(tclist):
    tableList = []
    uTableList = [item[0] for item in tclist]
    for i in uTableList:
        if i not in tableList:
            tableList.append(i)
    return tableList

def getColumnNames(tclist):
    uColumnList = [item[1] for item in tclist]
    return uColumnList


#Retrieves the Views accessable by the user
def getViewNames(username, password):
    try:
        conn = pymysql.connect("datasparkdb.cbbvbxlm9nap.us-east-1.rds.amazonaws.com", user=username,port=3306,passwd=password, db="DataSparkDataBase")
        stmnt = "SHOW FULL TABLES IN DataSparkDataBase WHERE TABLE_TYPE LIKE 'VIEW';"
        with conn.cursor() as cursor:
            sql = stmnt
            cursor.execute(sql)
    finally:
        closeMySqlConnection(conn)
    viewNames = [i[0] for i in cursor.fetchall()]
    return viewNames
    


# viewname is a list of views
def viewsDelete(username, password, viewname): 
    try:
        conn = pymysql.connect("datasparkdb.cbbvbxlm9nap.us-east-1.rds.amazonaws.com", user=username,port=3306,passwd=password, db="DataSparkDataBase")
        stmnt = "Drop VIEW if exists "
        for i in viewname:
            stmnt= stmnt + i +", " 
        stmnt = stmnt[:-2]
        with conn.cursor() as cursor:
            sql = stmnt
            cursor.execute(sql)
    finally:
        closeMySqlConnection(conn)
        return "views Deleted"
     

#This function deletes all the views created by the user and deletes the user itself.
def userDelete(username, password):
    try:
        conn = makeConnection()
        stmnt_1 = "DROP USER IF EXISTS '"+username+"'@'%' ;"
        userViews = getViewNames(username, password)
        UserViews_deleteStatus = viewsDelete(username, password, userViews)
        
        with conn.cursor() as cursor:
            sql = stmnt_1
            cursor.execute(sql)
    finally:
        closeMySqlConnection(conn)
    
            
 # This function updates the user's password.
def userUpdatePassword(username, newPassword):
    try:
        conn = makeConnection()
        stmnt = "ALTER USER '"+username+"'@'%' identified by '"+newPassword+"';"
        
        with conn.cursor() as cursor:
            sql = stmnt
            cursor.execute(sql)
    finally:
        closeMySqlConnection(conn)
    a = username+ " password updated"
    return a