from airium import Airium
# Import date class from datetime module
from datetime import datetime
from ReadConfig2 import getSQLCONFIG
import pyodbc
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine


configFilePath = r'C:\Users\akdmille\Documents\Python Files\configDEV72.ini'


c = getSQLCONFIG(configFilePath)

currentTableName = 'OB_GC_HNS_CompleteDate'
currentSchemaName = 'Enrollment'

dfColumnDetailParamString = "EXEC [dbo].[usp_WBTableDetails] @DatabaseName = N'NRTCUSTOMDB', @TableName = N'" + currentTableName + "', @Schema = N'" + currentSchemaName + "'"
dfTableSpecsParamString = "EXEC [dbo].[usp_WBTableSpecs] @DBName = N'NRTCUSTOMDB', @TableName = N'" + currentTableName + "', @SchemaName = N'" + currentSchemaName + "'"
dfIndexDetailParamString = "EXEC [dbo].[usp_WBIndexDetails] @DatabaseName = N'NRTCUSTOMDB', @TableName = N'" + currentTableName + "', @Schema = N'" + currentSchemaName + "'"

params = ("DRIVER={SQL Server};SERVER=dev_72.sql.caresource.corp\dev_72;DATABASE=ChangeTracking;Trusted_Connection=yes")

print(dfColumnDetailParamString)
print(dfTableSpecsParamString)
print(dfIndexDetailParamString)

try:
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
    with engine.begin() as conn:
      print('Connected to database')
      
      #Build the three dataframes

      dfColumnDetails = pd.DataFrame(conn.execute(dfColumnDetailParamString))
      if dfColumnDetails.empty:
         print('ColumnDetails DataFrame is empty!')
      else:   
        print(len(dfColumnDetails))
   
      dfTableSpecs = pd.DataFrame(conn.execute(dfTableSpecsParamString))
      if dfTableSpecs.empty:
         #print('TableSpec DataFrame is empty!')

         dfTableSpecs = pd.DataFrame({'PartitionRows': pd.Series(dtype='int'),
                   'CreatedDate': pd.Series(dtype='object'),
                   'ModifiedDate': pd.Series(dtype='object')            
                   })
         list = [ 0, 0, 0]
         dfTableSpecs.loc[len(dfTableSpecs)] = list   

      else:   
        print(len(dfTableSpecs))


      dfIndexDetail = pd.DataFrame(conn.execute(dfIndexDetailParamString))
      if dfIndexDetail.empty:
         #print('IndexDetail DataFrame is empty!')
         
         dfIndexDetail = pd.DataFrame({'TABLE_NAME': pd.Series(dtype='str'),
                   'COLUMN_NAME': pd.Series(dtype='str'),
                   'IndexName': pd.Series(dtype='str'),
                   'IndexID': pd.Series(dtype='int'),
                   'IndexColumnID': pd.Series(dtype='int'),
                   'IndexType': pd.Series(dtype='int')               
                   })


         list = [currentTableName, 'Null', 'Null', 0, 0, 0]
         dfIndexDetail.loc[len(dfIndexDetail)] = list     
          
      else:   
        print(len(dfTableSpecs))

      conn.close
      engine.dispose


except SQLAlchemyError as e:
         error = str(e.__dict__['orig'])
         print('database error ', e.args)
         print('Database connection error')  
         engine.dispose



