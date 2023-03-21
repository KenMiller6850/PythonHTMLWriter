from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from ReadConfig2 import getSQLCONFIG
from airium import Airium
import pandas as pd

a = Airium()

configFilePath = r'C:\Users\akdmille\Documents\Python Files\configDEV72.ini'
c = getSQLCONFIG(configFilePath)
params = ("DRIVER={SQL Server};SERVER=dev_72.sql.caresource.corp\dev_72;DATABASE=ChangeTracking;Trusted_Connection=yes")

try:
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
    with engine.begin() as conn:
      print('Connected to database')


    # write the SQL query inside the text() block
    sql = text('SELECT DISTINCT [DBName] FROM [ChangeTracking].[dbo].[AllDBTableReference]')
    #results = engine.execute(sql)

    dfDistinctDBNames = pd.read_sql(sql, engine)

    with a.div():
       a('Database Level')
       i = 0
       while i < len(dfDistinctDBNames.index): 
          with a.ul():
       
             with a.li(klass='level-1 db'):
                with a.div():
                  DBName = dfDistinctDBNames.iloc[i, dfDistinctDBNames.columns.get_loc('DBName')]
                  a.a(href='#' + DBName + "", _t='' +  DBName )  
                  
                  sqlTables = text("""SELECT DISTINCT [SchemaName],[TableName],[SchemaName] + '.' + [TableName] AS FullName
                                   FROM [ChangeTracking].[dbo].[AllDBTableReference]
                                   WHERE DBName = '""" + DBName + "'")
                  
                  
                  dfTableNames = pd.read_sql(sqlTables, engine)
             
                b = 0
                while b < len(dfTableNames.index): 
                  with a.ul():
                    with a.li(klass='level-1 db'):
                      with a.div():
                        TableName = dfTableNames.iloc[b, dfTableNames.columns.get_loc('FullName')]
                        a.a(href='#' + TableName + "", _t='' +  TableName )  
                    b += 1     
                  #print(dfTableNames) 

                i += 1

        

    #print(df)

except SQLAlchemyError as e:
    error = str(e.__dict__['orig'])
    print('database error ', e.args)
    print('Database connection error')  
    engine.dispose

html = str(a) # casting to string extracts the value

with open('C:\\Users\\akdmille\\Documents\\My Database Documentation\\FileTesting3\\User_databases\\NRTCUSTOMDB\\Tables\\treetest1.html', 'wb') as f:
    f.write(bytes(html, encoding="utf-8"))