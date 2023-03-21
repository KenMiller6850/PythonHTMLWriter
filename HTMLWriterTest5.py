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

#conn = pyodbc.connect('Driver={SQL Server};'
#                      'Server='+c[1]+';'
#                      'Database='+c[0]+';'
#                      'Trusted_Connection=yes;')


params = ("DRIVER={SQL Server};SERVER=dev_72.sql.caresource.corp\dev_72;DATABASE=ChangeTracking;Trusted_Connection=yes")

try:
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params) 
    with engine.begin() as conn:
      print('Connected to database')
      result = conn.execute("EXEC [dbo].[usp_WBTableDetails] @DatabaseName = N'NRTCUSTOMDB', @TableName = N'Network_Ops_Provider_Network_Prefix_Info', @Schema = N'dbo'")
      
      dftemp = pd.DataFrame(result)

      

      #for row in result:
      #  print((row['COLUMN_NAME'], row['ORDINAL_POSITION']))
      
      conn.close
      engine.dispose

except SQLAlchemyError as e:
  error = str(e.__dict__['orig'])
  print('database error ', e.args)
  print('Database connection error')  


engine.dispose

#Manipulate the dataframe


dftemp['COLUMN_DEFAULT'] = dftemp['COLUMN_DEFAULT'].replace(['(getdate())'], 'Current Date/Time')
dftemp['CHARACTER_MAXIMUM_LENGTH'] = dftemp['CHARACTER_MAXIMUM_LENGTH'].fillna(0)
dftemp['CHARACTER_MAXIMUM_LENGTH'] = dftemp['CHARACTER_MAXIMUM_LENGTH'].astype(int)



# datetime object containing current date and time
now = datetime.now()
 
# dd/mm/YY H:M:S
#dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
dt_string = now.strftime("%B %d %Y %H:%M:%S")
#print("date and time =", dt_string)

df = dftemp.sort_values(by=['ORDINAL_POSITION'])

print(df[['COLUMN_NAME','ORDINAL_POSITION']])


def addChangedRow(i):
    with a.tr(klass='changed'):
                                 
        with a.td():
               if df.iloc[i, df.columns.get_loc('IndexType')] == 1:
                 titleString = df.iloc[i, df.columns.get_loc('IndexName')]
                 a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)
        
               if df.iloc[i, df.columns.get_loc('IndexType')] > 1:
                 titleString = df.iloc[i, df.columns.get_loc('IndexName')]
                 a.img(a.img(alt='Indexes IDX_N_ID', klass='Index', src='../../../Images/Index.png', title= titleString))

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


def addNormalRow(i):
    with a.tr():
                                 
        with a.td():
               #a.div(_t=df.iloc[i, df.columns.get_loc('IndexName')])
               if df.iloc[i, df.columns.get_loc('IndexType')] == 1:
                 titleString = df.iloc[i, df.columns.get_loc('IndexName')]
                 a.img(alt='Clustered Index', klass='cluster', src='../../../Images/cluster.png', title= titleString)
        
               if df.iloc[i, df.columns.get_loc('IndexType')] > 1:
                 titleString = df.iloc[i, df.columns.get_loc('IndexName')]
                 a.img(a.img(alt='Indexes IDX_N_ID', klass='Index', src='../../../Images/Index.png', title= titleString))





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

a = Airium()

a('<!DOCTYPE html>')
with a.html(id="index"):
    with a.head():
        a.meta(charset="utf-8")
        a.title(_t="dbo.PaymentSettlementClaims")
        a.link(href='../../../Style/Master.css', rel='stylesheet', type='text/css')
        a.script(src='../../../Scripts/jquery-1.9.1.js', type='text/javascript')
        a.script(src='../../../Scripts/sections.js', type='text/javascript')

    with a.body():
        with a.div(id='wrap'):
            with a.div(id='container'):
                with a.div(id='header'):
                    a.div(id='breadcrumbs')
                    a.div(id='headerText')
                with a.div(id='pageTitle'):
                    a.img(alt='Tables', klass='Table32', src='../../../Images/Table32.png', title='Tables')
                    a('[dbo].[PaymentSettlementClaims]')
                with a.div(klass='panel panel-default panel-collapsible'):
                    with a.div(klass='panel-heading'):
                        with a.div(klass='expandCollapse'):
                            a.img(alt='collapsed', klass='collapsed', src='../../../Images/collapsed.png', style='display:none;', title='collapsed')
                            a.img(alt='expanded', klass='expanded', src='../../../Images/expanded.png', style='', title='expanded')
                        a.a(name='properties', _t='Table Properties')
                    with a.div(klass='panel-body'):
                        with a.table(border='0', cellspacing='1', klass='dataTable table-hover'):
                            with a.tbody():
                                with a.tr():
                                    a.th(_t='Property')
                                    a.th(_t='Value')
                                with a.tr():
                                    a.td(_t='Collation')
                                    a.td(_t='Latin1_General_BIN')
                                with a.tr():
                                    a.td(_t='Row Count (~)')
                                    a.td(_t='46')
                                with a.tr():
                                    a.td(_t='Created')
                                    a.td(_t='8:09:38 PM Tuesday, November 17, 2020')
                                with a.tr():
                                    a.td(_t='Last Modified')
                                    a.td(_t='8:09:38 PM Tuesday, November 17, 2020')

                with a.div(klass='panel panel-default panel-collapsible'):
                    with a.div(klass='panel-heading'):
                        with a.div(klass='expandCollapse'):
                            a.img(alt='collapsed', klass='collapsed', src='../../../Images/collapsed.png', style='display:none;', title='collapsed')
                            a.img(alt='expanded', klass='expanded', src='../../../Images/expanded.png', style='', title='expanded')
                        a.a(name='columns', _t='Column Specifications')
                    with a.div(klass='panel-body'):
                        with a.table(border='0', cellspacing='1', klass='dataTable table-hover', id="columnsTable"):

                            with a.tbody():
                                with a.div():
                                  with a.tr():
                                    a.th(_t='Key')
                                    a.th(_t='Name')
                                    a.th(_t='Data Type')
                                    a.th(_t='Max Length (Bytes)')
                                    with a.th():
                                        with a.div():
                                            a('Null Allowed')
                                            with a.a(href='#', title='Find information on the NULL option here.'):
                                                a.img(height='18', src='./CARESOURCE_jmmcabe.OLE DB Destination_files/questionmark.png', width='18')
                                    a.th(_t='Default Value')
                                    a.th(_t='Identity Column')
                                    

                                    
                                    i = 0
                                    while i < len(df.index):
                                         if df.iloc[i, df.columns.get_loc('DATA_TYPE')] == 'int':
                                           addChangedRow(i)
                                           #print(i)
                                         else:  
                                            addNormalRow(i)
                                            #print(i)
                                         i += 1 
   
                with a.div(klass='panel panel-default panel-collapsible'):
                    with a.div(klass='panel-heading'):
                        with a.div(klass='expandCollapse'):
                            a.img(alt='collapsed', klass='collapsed', src='../../../Images/collapsed.png', style='display:none;', title='collapsed')
                            a.img(alt='expanded', klass='expanded', src='../../../Images/expanded.png', style='', title='expanded')
                        a.a(name='indexes', _t='Indexes')
                    with a.div(klass='panel-body'):
                        with a.table(border='0', cellspacing='1', klass='dataTable table-hover'):
                            with a.tbody():
                                with a.tr():
                                    a.th(_t='Key')
                                    a.th(_t='Name')
                                    a.th(_t='Key Columns')
                                with a.tr():
                                    with a.td():
                                        with a.a(href='#indexes'):
                                            a.img(alt='Cluster Key IDX_ID: ID\\Prov_Ntwrk_Participation_Type1\\Prov_Ntwrk_Pfx_Code\\Active_Indicator', klass='cluster', src='../../../Images/cluster.png', title='Cluster Key IDX_ID: ID\\Prov_Ntwrk_Participation_Type1\\Prov_Ntwrk_Pfx_Code\\Active_Indicator')
                                    a.td(_t='IDX_ID')
                                    a.td(_t='ID, Prov_Ntwrk_Participation_Type1, Prov_Ntwrk_Pfx_Code, Active_Indicator')
                                with a.tr():
                                    a.td()
                                    a.td(_t='IDX_N_ID')
                                    a.td(_t='Prov_Prdct_State, Program_Type, Product_Type, Prov_Ntwrk_Pfx_Desc, Entity_K, Group_ID')                                         

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
                            a.img(alt='collapsed', klass='collapsed', src='./CARESOURCE_jmmcabe.OLE DB Destination_files/collapsed.png', style='display:none;', title='collapsed')
                            a.img(alt='expanded', klass='expanded', src='./CARESOURCE_jmmcabe.OLE DB Destination_files/expanded.png', style='', title='expanded')
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

with open('C:\\Users\\akdmille\\Documents\\My Database Documentation\\FileTesting3\\User_databases\\NRTCUSTOMDB\\Tables\\filetest3.html', 'wb') as f:
    f.write(bytes(html, encoding="utf-8"))



#with open('C:\\Users\\akdmille\\Documents\\Python Files\\pythonHTMLWriter\\Outputtest1.html', 'wb') as f:
#    f.write(bytes(html))