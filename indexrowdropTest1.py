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

c = getSQLCONFIG(configFilePath)


# datetime object containing current date and time
now = datetime.now()
 
# dd/mm/YY H:M:S
#dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
dt_string = now.strftime("%B %d %Y %H:%M:%S")
#print("date and time =", dt_string)

#currentTableName = 'Network_Ops_Provider_Network_Prefix_Info'
#currentSchemaName = 'dbo'

currentTableName = 'CAQH_COB_InboundTransaction'
currentSchemaName = 'Enrollment'

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
      if dfColumnDetails.empty:
         print('ColumnDetails DataFrame is empty!')
      else:   
        dfColumnDetails['IdentityColumn'] = dfColumnDetails['IdentityColumn'].fillna(0)
        dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'] = dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'].fillna(0)
        dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'] = dfColumnDetails['CHARACTER_MAXIMUM_LENGTH'].astype(int)
        dfColumnDetails = dfColumnDetails.sort_values(by=['ORDINAL_POSITION'])
        #print(len(dfColumnDetails))
        
        dfColumnDetails.sort_values(by='ORDINAL_POSITION', inplace=True)



   
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
         print('Heap Entry: ' + str(dfTableSpecs[dfTableSpecs.eq("HEAP").any(1)]))
         flagHeap = True




      dfIndexDetail = pd.DataFrame(conn.execute(dfIndexDetailParamString))
      if dfIndexDetail.empty:
         print('IndexDetail DataFrame is empty!')
         flagHeap = True
         #dfIndexDetail = pd.DataFrame({'TABLE_NAME': pd.Series(dtype='str'),
         #          'COLUMN_NAME': pd.Series(dtype='str'),
         #          'IndexName': pd.Series(dtype='str'),
         #          'IndexID': pd.Series(dtype='int'),
         #          'IndexColumnID': pd.Series(dtype='int'),
         #          'IndexType': pd.Series(dtype='int')               
         #          })


         #list = [currentTableName, 'Null', 'Null', 0, 0, 0]
         #dfIndexDetail.loc[len(dfIndexDetail)] = list   
         #print(dfIndexDetail)  
          
      else:   
        #print(dfIndexDetail)
        #index_names = dfIndexDetail[dfIndexDetail['IndexName'] == 'HEAP' ].index
        #dfIndexDetail.drop(index_names, inplace = True)
        #IndexCount = dfIndexDetail['IndexID'].max()
        IndexCount = len(pd.unique(dfIndexDetail['IndexID']))

        print('Index Count: ' + str(IndexCount))

      conn.close
      engine.dispose


except SQLAlchemyError as e:
         error = str(e.__dict__['orig'])
         print('database error ', e.args)
         print('Database connection error')  
         engine.dispose





#IndexCount = dfIndexDetail['IndexID'].max()
indexString = ''


#Create a DataFrame object
#This code extracts individual columns from an index and builds a single string for each index
#dfIndexDetailsCollapsed_cols = ['IndexName', 'IndexColumns']
#dfIndexDetailsCollapsed = pd.DataFrame()

#print('Index Detail: ' + dfIndexDetail)

#IndexColumnList = []
#print(dfIndexDetail)

#n = len(pd.unique(dfIndexDetail['IndexID']))
#print(n)
print(flagHeap)


""" i = 1

while i <= IndexCount:
    z = 0
    
    newdf = dfIndexDetail.query('IndexID == ' + str(i))


    while z < len(newdf.index):
        indexType = newdf.iloc[z, newdf.columns.get_loc('IndexType')] 
        indexString += newdf.iloc[z, newdf.columns.get_loc('COLUMN_NAME')] + ' - ' 
        indexName = newdf.iloc[z, newdf.columns.get_loc('IndexName')] 
        
        print(indexString)
        #s1 = pd.Series([indexName])
        #s2 = pd.Series(indexString.rstrip(indexString[-2]))
        #s3 = pd.Series([indexType])
        z += 1 
        
    #print(indexName) 
    IndexColumnList.append(indexString)
    indexString = ''
    #appended_series = pd.concat([s1,s2,s3],axis=1)  
    #dfIndexDetailsCollapsed = dfIndexDetailsCollapsed.append(appended_series, ignore_index=True)
       
  
  
    i += 1 

print(IndexColumnList)    
 """



