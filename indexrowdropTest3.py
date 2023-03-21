from airium import Airium
# Import date class from datetime module
from datetime import datetime
from ReadConfig2 import getSQLCONFIG
import pyodbc
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine


configFilePath = r'C:\Users\akdmille\Documents\Python Files\configDEV72.ini'
flagNoIndex = False
flagHeap = False
IndexCount = 0
IndexString = ''
ColumnDescripList = []
IndexTypeList = []
IndexNameList = []

c = getSQLCONFIG(configFilePath)


# datetime object containing current date and time
now = datetime.now()
 
# dd/mm/YY H:M:S
#dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
dt_string = now.strftime("%B %d %Y %H:%M:%S")
#print("date and time =", dt_string)

currentTableName = 'Network_Ops_Provider_Network_Prefix_Info'
currentSchemaName = 'dbo'

#currentTableName = 'CAQH_COB_InboundTransaction'
#currentSchemaName = 'Enrollment'
#currentSchemaName = 'Enrollment'

#currentTableName = 'Facets_ProviderSetupQualityCheck_Audit_Stg'
#currentSchemaName = 'dbo'



dfColumnDetailParamString = "EXEC [dbo].[usp_WBTableDetails] @DatabaseName = N'NRTCUSTOMDB', @TableName = N'" + currentTableName + "', @Schema = N'" + currentSchemaName + "'"
dfTableSpecsParamString = "EXEC [dbo].[usp_WBTableSpecs] @DBName = N'NRTCUSTOMDB', @TableName = N'" + currentTableName + "', @SchemaName = N'" + currentSchemaName + "'"
dfIndexDetailParamString = "EXEC [dbo].[usp_WBIndexDetails] @DatabaseName = N'NRTCUSTOMDB', @TableName = N'" + currentTableName + "', @Schema = N'" + currentSchemaName + "'"

params = ("DRIVER={SQL Server};SERVER=dev_72.sql.caresource.corp\dev_72;DATABASE=ChangeTracking;Trusted_Connection=yes")

#print(dfColumnDetailParamString)
#print(dfTableSpecsParamString)
#print(dfIndexDetailParamString)

try:
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
    with engine.begin() as conn:
      print('Connected to database')

      #Build the three dataframes

      dfColumnDetails = pd.DataFrame(conn.execute(dfColumnDetailParamString))
      dfTableSpecs = pd.DataFrame(conn.execute(dfTableSpecsParamString))
      dfIndexDetail = pd.DataFrame(conn.execute(dfIndexDetailParamString))



      if dfColumnDetails.empty:
         print('ColumnDetails DataFrame is empty!')
      else:   
        dfColumnDetails['IdentityColumn'] = dfColumnDetails['IdentityColumn'].fillna(0)
        dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'] = dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'].fillna(0)
        dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'] = dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'].astype(int)
        dfColumnDetails = dfColumnDetails.sort_values(by=['ORDINAL_POSITION'])
        #print(len(dfColumnDetails))
        
        dfColumnDetails.sort_values(by='ORDINAL_POSITION', inplace=True)
        

      
      
      
      if dfIndexDetail.empty:
         print('IndexDetail DataFrame is empty!')
         flagHeap = True

      else:   
        IndexCount = len(pd.unique(dfIndexDetail['IndexID']))
        print('Index Count: ' + str(IndexCount))
        #print(dfIndexDetail)
        #print(dfIndexDetail['IndexID'].unique())




      if dfTableSpecs.empty:
          print('TableSpec DataFrame is empty!')
          flagHeap = True
      #else:     
      #    print(dfTableSpecs) 







except SQLAlchemyError as e:
         error = str(e.__dict__['orig'])
         print('database error ', e.args)
         print('Database connection error')  
         engine.dispose


#
if not flagHeap:
   dfIndexDetailsCollapsed = pd.DataFrame(columns=['IndexColumnData','IndexType'])


   i = 1

   while i <= IndexCount:

     newdf = dfIndexDetail.query('IndexID == ' + str(i))
     #indexName = newdf.iloc[i, newdf.columns.get_loc('IndexName')] 
     #print(newdf)

     indexName = newdf.iloc[0,2]
     indexType = newdf.iloc[0,5]
     print('Index Type: ' + str(indexType))
     #df2 = newdf.iloc[:, 1]
  
     df2 = newdf.iloc[: ,1].copy()
     s= df2.str.cat(sep=',')
  
     #print(indexName + ': ' + s)

     #abc_series = pd.Series(s)

     ColumnDescripList.append(s)
     IndexTypeList.append(indexType)
     IndexNameList.append(indexName)

     #dfIndexDetailsCollapsed  = pd.DataFrame([indexName + ': ' + s, indexType], columns=['IndexColumnData', 'IndexType'])
       
     i += 1

print(IndexTypeList)

dfIndexDetailsCollapsed = pd.DataFrame(
    {'IndexColumns': ColumnDescripList,
     'IndexType': IndexTypeList,
     'IndexName' : IndexNameList
    })



#dfIndexDetailsCollapsed = pd.DataFrame(ColumnDescripList, IndexTypeList)

