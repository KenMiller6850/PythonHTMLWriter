import pandas as pd

dfIndexDetail = pd.DataFrame({'TABLE_NAME': pd.Series(dtype='str'),
                   'COLUMN_NAME': pd.Series(dtype='str'),
                   'IndexName': pd.Series(dtype='str'),
                   'IndexID': pd.Series(dtype='int'),
                   'IndexColumnID': pd.Series(dtype='int'),
                   'IndexType': pd.Series(dtype='int')               
                   })


list = [ 0, 0, 0]
dfIndexDetail.loc[len(dfIndexDetail)] = list     


print(dfIndexDetail)