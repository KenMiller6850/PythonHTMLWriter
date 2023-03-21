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
      else:     
          print(dfTableSpecs) 







except SQLAlchemyError as e:
         error = str(e.__dict__['orig'])
         print('database error ', e.args)
         print('Database connection error')  
         engine.dispose


#
dfIndexDetailsCollapsed = pd.DataFrame(columns=['IndexColumnData','IndexType'])


i = 1

while i <= IndexCount:

  newdf = dfIndexDetail.query('IndexID == ' + str(i))
  #indexName = newdf.iloc[i, newdf.columns.get_loc('IndexName')] 

  indexName = newdf.iloc[0,2]
  indexType = newdf.iloc[0,5]

  #df2 = newdf.iloc[:, 1]
  
  df2 = newdf.iloc[: ,1].copy()
  s= df2.str.cat(sep=',')
  
  #print(indexName + ': ' + s)

  #abc_series = pd.Series(s)

  ColumnDescripList.append(s)
  IndexTypeList.append(indexType)
  IndexNameList.append(indexName)


  i += 1


dfIndexDetailsCollapsed = pd.DataFrame(ColumnDescripList, columns=['IndexColumnData'])

dfIndexDetailsCollapsed = pd.DataFrame(
    {'IndexColumns': ColumnDescripList,
     'IndexType': IndexTypeList,
     'IndexName' : IndexNameList
    })

print (dfIndexDetailsCollapsed)






def addChangedRow(i):
    with a.tr(klass='changed'):

        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('ORDINAL_POSITION')])
                             
        with a.td():
               if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IndexType')] == 1:
                 a.div(_t='<i class="fas fa-key text-danger"></i>')

                 #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' clustered'
                 #a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)
        
               if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IndexType')] > 1:
                 a.div(_t='<i class="fas fa-project-diagram text-info"></i>')
                 #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' non-clustered'
                 #a.img(a.img(alt='Non-Clustered Index', klass='Index', src='../../../Images/Index.png', title= titleString))

        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_NAME')])

        with a.td():      
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('DATA_TYPE')])

        with a.td():     
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('CHARACTER_MAXIMUM_LENGTH')])

        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IS_NULLABLE')])

        with a.td():     
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_DEFAULT')])

        with a.td():     
            if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IdentityColumn')] == 1:
                 a.div(_t='<i class="fas fa-flag text-success"></i>')
                 #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' clustered'
                 #a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)


def addNormalRow(i):
    with a.tr():
                                 

        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('ORDINAL_POSITION')])

        with a.td():
               #a.div(_t=df.iloc[i, df.columns.get_loc('IndexName')])
               if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IndexType')] == 1:
                 a.div(_t='<i class="fas fa-key  text-danger"></i>')
                 #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' clustered'
                 #a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)
        
               if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IndexType')] > 1:
                 a.div(_t='<i class="fas fa-project-diagram text-info"></i>')
                 
                 #titleString = df.iloc[i, df.columns.get_loc('IndexName')] + ' non-clustered'
                 #a.img(a.img(alt='Non-Clustered Index', klass='Index', src='../../../Images/Index.png', title= titleString))


        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_NAME')])

        with a.td():      
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('DATA_TYPE')])

        with a.td():     
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('CHARACTER_MAXIMUM_LENGTH')])

        with a.td():   
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IS_NULLABLE')])

        with a.td():     
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('COLUMN_DEFAULT')])

        with a.td():     
            a.div(_t=dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('IdentityColumn')])       


def addClusteredIndexRow(i):
    with a.tr(klass='clustered'):
        with a.td():   
            #a.div(_t=dfIndexDetails.iloc[i, dfIndexDetails.columns.get_loc('IndexType')])
            a.div(_t='Clustered')

        with a.td():   
            a.div(_t=dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexName')])

        with a.td():   
            a.div(_t=dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexColumns')])


def addNCIndexRow(i):
    with a.tr():
        with a.td():   
            #a.div(_t='Non-Clustered')
            a.div(_t= '-') 

        with a.td():   
            a.div(_t=dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexName')])

        with a.td():   
            a.div(_t=dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexColumns')])            


a = Airium()

a('<!DOCTYPE html>')
with a.html(id="index"):
    with a.head():
        a.meta(charset="utf-8")
        a.title(_t="dbo.PaymentSettlementClaims")
        a.link(href='../../../Style/Master.css', rel='stylesheet', type='text/css')
        a.link(href='../../../vendor/fontawesome/all.min.css', rel='stylesheet', type='text/css' )
        a.script(src='../../../Scripts/jquery-1.9.1.js', type='text/javascript')
        a.script(src='../../../Scripts/sections.js', type='text/javascript')
        a.script(src='../../../Scripts/sortable.min.js', type='text/javascript')


    with a.body():
        with a.div(id='wrap'):
            with a.div(id='container'):
                with a.div(id='top-header', klass='image-text'):
                       a.img(alt='expanded', src='../../../Images/tableCS.png', style='')
                       a('<h1 style="color:gray; background-color: #ddbbff;border-radius: 6px;width: 1200px;box-shadow: 2px 2px 20px 5px #ddbbff">dbo.Network_Ops_Provider_Network_Prefix_Info</h1>')

                #with a.div(id='pageTitle'):
                    
                    
                    
                with a.div(klass='panel panel-default panel-collapsible'):
                    with a.div(klass='panel-heading'):
                        with a.div(klass='expandCollapse'):
                            #a.img(alt='collapsed', klass='collapsed', src='../../../Images/collapsed.png', style='display:none;', title='collapsed')
                            #a.img(alt='expanded', klass='expanded', src='../../../Images/expanded.png', style='', title='expanded')
                            a.a(name='properties', _t='Table Properties')
                    with a.div(klass='panel-body'):
                        with a.table(border='0', cellspacing='1', klass='dataTable table-hover'):
                            with a.tbody():
                                #with a.tr():
                                    #a.th(_t='Property')
                                    #a.th(_t='Value')
                                #with a.tr():
                                    #a.td(_t='Collation')
                                    #a.td(_t='Latin1_General_BIN')
                                with a.tr():
                                    a.td(_t='Row Count (~)')
                                    with a.td():
                                      a.div(_t=dfTableSpecs.iloc[0, dfTableSpecs.columns.get_loc('PartitionRows')])
                                with a.tr():
                                    a.td(_t='Created On')
                                    with a.td():
                                      a.div(_t=dfTableSpecs.iloc[0, dfTableSpecs.columns.get_loc('CreatedDate')])
                                with a.tr():
                                    a.td(_t='Last Modified')
                                    with a.td():
                                      a.div(_t=dfTableSpecs.iloc[0, dfTableSpecs.columns.get_loc('ModifiedDate')])

                with a.div(klass='panel panel-default panel-collapsible'):
                    with a.div(klass='panel-heading'):
                        with a.div(klass='expandCollapse'):
                            #a.img(alt='collapsed', klass='collapsed', src='../../../Images/collapsed.png', style='display:none;', title='collapsed')
                            #a.img(alt='expanded', klass='expanded', src='../../../Images/expanded.png', style='', title='expanded')
                            a.a(name='columns', _t='Column Specifications')
                    with a.div(klass='panel-body'):
                        with a.table(border='0', cellspacing='1', klass='sortable', id="columnsTable"):
                          with a.thead():
                            with a.tbody():
                                with a.div():
                                  with a.tr():
                                    a.th(_t='#')
                                    a.th(_t='Key')
                                    a.th(_t='Name')
                                    a.th(_t='Data Type')
                                    a.th(_t='Max Length (Bytes)')
                                    with a.th():
                                        with a.div():
                                            a('Null Allowed')
                                            with a.a(href='#', title='Find information on the NULL option here.'):
                                                a.img(_t='<i class="fa fa-question-circle fa-lg"></i>')
                                    a.th(_t='Default Value')
                                    a.th(_t='Identity Column')
                                    

                                    
                            i = 0
                            while i < len(dfColumnDetails.index):
                                if dfColumnDetails.iloc[i, dfColumnDetails.columns.get_loc('DATA_TYPE')] == 'int':
                                   addChangedRow(i)
                                    #print(i)
                                else:  
                                   addNormalRow(i)
                                   #print(i)
                                i += 1 
   
                with a.div(klass='panel panel-default panel-collapsible'):
                    with a.div(klass='panel-heading'):
                        with a.div(klass='expandCollapse'):
                            #a.img(alt='collapsed', klass='collapsed', src='../../../Images/collapsed.png', style='display:none;', title='collapsed')
                            #a.img(alt='expanded', klass='expanded', src='../../../Images/expanded.png', style='', title='expanded')
                            a.a(name='indexes', _t='Index Details')
                    with a.div(klass='panel-body'):
                        with a.table(border='0', cellspacing='1', klass='dataTable table-hover'):
                            with a.tbody():
                                with a.tr():
                                    a.th(_t='Type')
                                    a.th(_t='Name')
                                    a.th(_t='Key Columns')
 
                            i = 0
                            while i < len(dfIndexDetailsCollapsed.index):
                                if dfIndexDetailsCollapsed.iloc[i, dfIndexDetailsCollapsed.columns.get_loc('IndexType')] == 1:
                                   addClusteredIndexRow(i)
                                    #print(i)
                                else:  
                                   addNCIndexRow(i)
                                   #print(i)
                                i += 1 












"""                                          if df.iloc[i, df.columns.get_loc('DATA_TYPE')] == 'int':
                                            addChangedRow(i)
                                    else:
                                         if df.iloc[i, df.columns.get_loc('DATA_TYPE')] == 'int':
                                             addNormalRow(i)
                                             
                                         print(i)
                                         i += 1  """
                                         
                                       #print(df.iloc[i, df.columns.get_loc('COLUMN_NAME')])    
"""                                          with a.tr(klass='changed'):
                                          
                                         #a.td()
                                          with a.td():
                                            a.div()

                                          with a.td():   
                                            a.div(_t=df.iloc[i, df.columns.get_loc('COLUMN_NAME')])

                                          with a.td():      
                                            a.div(_t=df.iloc[i, df.columns.get_loc('DATA_TYPE')])

                                          with a.td():     
                                            a.div(_t=df.iloc[i, df.columns.get_loc('CHARACTER_MAXIMUM_LENGTH')])

                                          with a.td():   
                                            a.div(_t=df.iloc[i, df.columns.get_loc('IS_NULLABLE')])

                                          with a.td():     
                                            a.div(_t=df.iloc[i, df.columns.get_loc('COLUMN_DEFAULT')])

                                          with a.td():     
                                            a.div() 
                                         """


with a.div(klass='panel panel-default panel-collapsible'):
                    with a.div(klass='panel-heading'):
                        with a.div(klass='expandCollapse'):
                            #a.img(alt='collapsed', klass='collapsed', src='./CARESOURCE_jmmcabe.OLE DB Destination_files/collapsed.png', style='display:none;', title='collapsed')
                            #a.img(alt='expanded', klass='expanded', src='./CARESOURCE_jmmcabe.OLE DB Destination_files/expanded.png', style='', title='expanded')
                            a.a(name='uses', _t='Uses')
                    with a.div(klass='panel-body'):
                        with a.ul(klass='DependencyList'):
                            with a.li():
                                with a.a(href='https://caresource.sharepoint.com/sites/SQLAssistance/DataDictionary/DEV72Docs/User_databases/NRTCUSTOMDB/Security/Schemas/CARESOURCE_jmmcabe_CARESOURCE_jmmcabe.aspx'):
                                    a('CARESOURCE\\jmmcabe')
with a.div(id='footer'):
            with a.div(klass='row'):
                with a.div(klass='col-sm-4', id='customtext'):
                    a.div(id='projectauthor', _t='CareSource Database Engineering')
                a.div(klass='col-sm-4', id='copyright', _t='Part of the Data Dictionary Project')
                a.div(klass='col-sm-4', id='date', _t='Created: ' + dt_string )









html = str(a) # casting to string extracts the value

#print(html)

with open('C:\\Users\\akdmille\\Documents\\My Database Documentation\\FileTesting3\\User_databases\\NRTCUSTOMDB\\Tables\\' + currentTableName + 'Test.html', 'wb') as f:
    f.write(bytes(html, encoding="utf-8"))

with open('C:\\Users\\akdmille\\Documents\\My Database Documentation\\FileTesting3\\User_databases\\NRTCUSTOMDB\\Tables\\' + currentTableName + 'Test.aspx', 'wb') as f:
    f.write(bytes(html, encoding="utf-8"))    
