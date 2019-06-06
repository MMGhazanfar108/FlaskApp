
# coding: utf-8

# In[81]:


import pandas as pd
import pymysql


# In[82]:


def openMySqlConnection(host, port, dbname, user, password):
    conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
    print("The connection is open")
    return conn


# In[83]:


def closeMySqlConnection():
    conn.close()
    print("The connection is closed")


# In[84]:


def createUser(conn, userName, userPass):
    try:
        stmntNewUser = "CREATE USER '" + userName + "'@'%'" + " IDENTIFIED BY '" + userPass + "';"
        with conn.cursor() as cursor:
            sql = stmntNewUser
            print(sql)
            cursor.execute(sql)

        with conn.cursor() as cursor:
            sql = "SELECT user FROM mysql.user"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    finally:
        print("User created")


# In[85]:


def createView(tableName, viewName, columns):
    stmnt = "CREATE VIEW " + viewName + " AS SELECT " + columns + " FROM " + tableName + ";"
    try:
        with conn.cursor() as cursor:
            cursor.execute(stmnt)
    finally:
        print("View created")


# In[86]:


def createViewTables(conn, tablenames, columnNames, viewName):
    try:
        print(columnNames)
        print(tablenames)
        stmt = "Create view " + viewName + " as select " + tablenames[0]+".POA_CODE_2016, "
        for i in columnNames:
            if(i!="POA_CODE_2016"):
                stmt += i + ", "
        stmt=stmt[:-2]
        stmt+= " from "
        for i in tablenames:
            stmt+= i + ", "
        stmt=stmt[:-2]
        if(len(tablenames)>1):
            stmt+= " where "
            for j in range(len(tablenames)-1):
               stmt+= tablenames[0]+".POA_CODE_2016 = " + tablenames[j+1] + ".POA_CODE_2016 AND "
        stmt=stmt[:-4]
        with conn.cursor() as cursor:
            print(stmt)
            cursor.execute(stmt)
            "Executing statement..."
    finally:
        print("View created")


# In[87]:


def grantPermissions(databaseName, viewName, userName):
    stmnt = "GRANT ALL ON " + databaseName + "." + viewName + " TO '" + userName + "'@'%';"
    try:
        with conn.cursor() as cursor:
            sql = stmnt
            cursor.execute(sql)
    finally:
        print("Permission given")


# In[88]:


def revokePermissions(userName):
    stmnt = "REVOKE ALL PRIVILEGES ON *.* FROM '" + userName + "'@'%';"
    try:
        with conn.cursor() as cursor:
            sql = stmnt
            cursor.execute(sql)
    finally:
        print("Permissions revoked")


# In[70]:

# In[89]:


def newAccess(username, userpass, tablesColumnList):
    host = "datasparkdb.cbbvbxlm9nap.us-east-1.rds.amazonaws.com"
    port = 3306
    dbname = "DataSparkDataBase"
    user = "aarasu"
    password = "aabbccdd1234"

    conn = openMySqlConnection(host, port, dbname, user, password)
    createUser(conn, username, userpass)
    viewName = username + "_selected_tables_columns"
    print(viewName)
    createViewTables(conn, getTableNames(tablesColumnList), getColumnNames(tablesColumnList), viewName)
    grantPermissions("DataSparkDataBase", viewName, username)
    conn.close()


# In[94]:


#newAccess("erick", "1234", [["2016Census_G04A_AUS_POA", "Age_yr_1_M"], ["2016Census_G04B_AUS_POA","Age_yr_60_M"]])


# In[90]:


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


if __name__ == "__main__":
    newAccess("mustafa2", "1234", [["2016Census_G04A_AUS_POA", "Age_yr_1_M"], ["2016Census_G04B_AUS_POA","Age_yr_60_M"]])
