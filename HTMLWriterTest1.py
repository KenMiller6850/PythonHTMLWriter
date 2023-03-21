from airium import Airium
# Import date class from datetime module
from datetime import datetime
from ReadConfig2 import getSQLCONFIG
import pyodbc
import pandas as pd


configFilePath = r'C:\Users\akdmille\Documents\Python Files\configDEV72.ini'


c = getSQLCONFIG(configFilePath)

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server='+c[1]+';'
                      'Database='+c[0]+';'
                      'Trusted_Connection=yes;')



query = """SELECT [DBCaptureID],[TABLE_CATALOG],[TABLE_SCHEMA]
      ,[TABLE_NAME],[COLUMN_NAME],[ORDINAL_POSITION],[COLUMN_DEFAULT]
      ,[IS_NULLABLE]
      ,[DATA_TYPE]
      ,[CHARACTER_MAXIMUM_LENGTH]
      ,[COLLATION_NAME]

  FROM [ChangeTracking].[dbo].[CTColumns]
  WHERE TABLE_CATALOG = 'NRTCUSTOMDB'
  and TABLE_NAME = 'Cactus_Associate_List'
  AND DBCaptureID = 20"""

df = pd.read_sql(query, conn)
#print(df)
conn.close()

#Manipulate the dataframe
df['COLUMN_DEFAULT'] = df['COLUMN_DEFAULT'].replace(['(getdate())'], 'Current Date/Time')
df['CHARACTER_MAXIMUM_LENGTH'] = df['CHARACTER_MAXIMUM_LENGTH'].fillna(0)
df['CHARACTER_MAXIMUM_LENGTH'] = df['CHARACTER_MAXIMUM_LENGTH'].astype(int)


# datetime object containing current date and time
now = datetime.now()
 
# dd/mm/YY H:M:S
#dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
dt_string = now.strftime("%B %d %Y %H:%M:%S")
#print("date and time =", dt_string)


a = Airium()

a('<!DOCTYPE html>')
with a.html(id="index"):
    with a.head():
        a.meta(charset="utf-8")
        a.title(_t="dbo.Cactus_Associate_List")
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
                    a('[dbo].[Cactus_Associate_List]')
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
                        a.a(name='columns', _t='Columns')
                    with a.div(klass='panel-body'):
                        with a.table(border='0', cellspacing='1', klass='dataTable table-hover'):
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
                                                a.img(height='12', src='./CARESOURCE_jmmcabe.OLE DB Destination_files/questionmark.png', width='12')
                                    a.th(_t='Default Value')
                                    a.th(_t='Identity Column')
                                    
                                with a.tr():
                                  with a.td():
                                    
                                    i = 0
                                    while i < len(df.index):
                                        columnName = df.iloc[i, df.columns.get_loc('COLUMN_NAME')]
                                        with a.tr():
                                          a.td()
                                          a.td(_t=df.iloc[i, df.columns.get_loc('COLUMN_NAME')])
                                          a.td(_t=df.iloc[i, df.columns.get_loc('DATA_TYPE')])
                                          a.td(_t=df.iloc[i, df.columns.get_loc('CHARACTER_MAXIMUM_LENGTH')])
                                          a.td(_t=df.iloc[i, df.columns.get_loc('IS_NULLABLE')])
                                          a.td(_t=df.iloc[i, df.columns.get_loc('COLUMN_DEFAULT')])
                                          a.td()
                                          i += 1



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

with open('C:\\Users\\akdmille\\Documents\\My Database Documentation\\FileTesting3\\User_databases\\NRTCUSTOMDB\\Tables\\filetest.html', 'wb') as f:
    f.write(bytes(html, encoding="utf-8"))



#with open('C:\\Users\\akdmille\\Documents\\Python Files\\pythonHTMLWriter\\Outputtest1.html', 'wb') as f:
#    f.write(bytes(html))