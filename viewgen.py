from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import numpy as np
#%config IPCompleter.greedy=True


def stmtfc(tablenames, columnNames, viewName, username, password):
    connect_stmt="mysql+mysqlconnector://"+username+":"+password+"@localhost/ds_db_schema?host=localhost?port=3306"
    engine_Func = create_engine(connect_stmt)
    stmt = "Create view "
    stmt+= viewName
    stmt+= " as select "
    stmt+= tablenames[0]+".POA_CODE_2016, "
    for i in columnNames:
        if(i!="POA_CODE_2016"):
            stmt+= i+", "
    stmt=stmt[:-2]
    stmt+= " from "
    for i in tablenames:
        stmt+= i+", "
    stmt=stmt[:-2]
    if(len(tablenames)>1):
        stmt+= " where "
        for j in range(len(tablenames)-1):
           stmt+= tablenames[0]+".POA_CODE_2016 = "+tablenames[j+1]+".POA_CODE_2016 AND "
    stmt=stmt[:-4]
    with engine_Func.connect() as con:
        rs = con.execute(stmt)
    engine_Func.dispose()
    a= "completed"
    return a
    