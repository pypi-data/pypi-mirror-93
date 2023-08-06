# villaInventorySdk



full docs here https://thanakijwanavit.github.io/villa-inventory-sdk/

## Install

`pip install villaInventorySdk`

## How to use

Uploading a large amount of data

## sample input

```python
from villaPricingSdk.price import PricingSdk
from random import randrange
import boto3, time, json
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
import pandas as pd
from nicHelper.dictUtil import printDict
```

```python
sampleInput =  [
               {
                  'cprcode': 9,
                  'brcode': 1000,
                  'price': 50
                },
               {
                  'cprcode': 4,
                  'brcode': 1000,
                  'price': 35
               },
                {
                  'cprcode': 3,
                  'brcode': 1003,
                  'price': 36,
               }
              ]
def getDf(input_:dict):
  return pd.DataFrame(input_)
  
df = getDf(sampleInput)
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cprcode</th>
      <th>brcode</th>
      <th>price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>9</td>
      <td>1000</td>
      <td>50</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4</td>
      <td>1000</td>
      <td>35</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1003</td>
      <td>36</td>
    </tr>
  </tbody>
</table>
</div>



## Upload data

## init sdk

## Update price 

```python
%%time
key = 'test'
r = sdk.uploadDf(df, key = key)
if r.status_code >= 400: raise Exception(r.json())
sdk.ingestData(key = key)
```

    signed url is 
    url : https://pr
    fields
     key : test
     AWSAccessKeyId : ASIAVX4Z5T
     x-amz-security-token : IQoJb3JpZ2
     policy : eyJleHBpcm
     signature : kgDRy1etYA
    CPU times: user 44.1 ms, sys: 4.2 ms, total: 48.3 ms
    Wall time: 5.47 s





    {'body': '{"cprcode":{"0":9,"1":4,"2":3},"brcode":{"0":1000,"1":1000,"2":1003},"price":{"0":50,"1":35,"2":36}}',
     'statusCode': 200,
     'headers': {'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': '*'}}



## Query single product

```python
%%time
sdk.querySingleProduct2(cprcode=1234)
```

    succesfully get url, returning pandas
    CPU times: user 20.5 ms, sys: 0 ns, total: 20.5 ms
    Wall time: 2.69 s





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cprcode</th>
      <th>brcode</th>
      <th>price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>1234.0</td>
      <td>1000.0</td>
      <td>123.0</td>
    </tr>
  </tbody>
</table>
</div>



## Query Branch

```python
%%time
sdk.branchQuery(1000)
```


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    <timed eval> in <module>


    ~/SageMaker/.persisted_conda/python38/lib/python3.8/site-packages/nicHelper/wrappers.py in wrapper(self, *args, **kwargs)
         12         @wraps(func)
         13         def wrapper(self, *args, **kwargs):
    ---> 14             return func(self, *args, **kwargs)
         15         setattr(cls, func.__name__, wrapper)
         16         # Note we are not binding func, but wrapper which accepts self but does exactly the same as func


    ~/SageMaker/stacks/villaMaster/villa-master-dev/price/villa-price-sdk/villaPricingSdk/price.py in branchQuery(self, brcode, cprcodes)
        151   })
        152   rawReturn = lambda_.invoke(functionName=self.endpoint.queryBranch(), input = payload)
    --> 153   parsedReturn = Response.parseBody(rawReturn)
        154   return pd.read_feather(parsedReturn['url'])
        155 


    ~/SageMaker/.persisted_conda/python38/lib/python3.8/site-packages/awsSchema/apigateway.py in parseBody(cls, dictInput)
         22   @classmethod
         23   def parseBody(cls, dictInput:dict):
    ---> 24     response = cls.fromDict(dictInput)
         25     return response.body
         26 


    ~/SageMaker/.persisted_conda/python38/lib/python3.8/site-packages/awsSchema/apigateway.py in fromDict(cls, dictInput)
         31       dictInput should follow apigateway proxy integration
         32     '''
    ---> 33     body = dictInput.pop('body')
         34     return cls(
         35       body = json.loads(body),


    KeyError: 'body'


## Query All

```python
%%time
sdk.queryAll2()
```

    succesfully get url, returning pandas
    CPU times: user 17.1 ms, sys: 137 µs, total: 17.2 ms
    Wall time: 221 ms





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cprcode</th>
      <th>brcode</th>
      <th>price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10806.0</td>
      <td>1010.0</td>
      <td>513.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>89190.0</td>
      <td>1028.0</td>
      <td>869.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>41962.0</td>
      <td>1021.0</td>
      <td>920.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>88179.0</td>
      <td>1004.0</td>
      <td>725.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1234.0</td>
      <td>1000.0</td>
      <td>123.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>12345.0</td>
      <td>1000.0</td>
      <td>345.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>19163.0</td>
      <td>1027.0</td>
      <td>745.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>55427.0</td>
      <td>1022.0</td>
      <td>561.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>35004.0</td>
      <td>1002.0</td>
      <td>625.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>4.0</td>
      <td>1000.0</td>
      <td>35.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>4.0</td>
      <td>1000.0</td>
      <td>35.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>4.0</td>
      <td>1000.0</td>
      <td>35.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>4.0</td>
      <td>1000.0</td>
      <td>35.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>9.0</td>
      <td>1000.0</td>
      <td>50.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>9.0</td>
      <td>1000.0</td>
      <td>50.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>9.0</td>
      <td>1000.0</td>
      <td>50.0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>9.0</td>
      <td>1000.0</td>
      <td>50.0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>23505.0</td>
      <td>1000.0</td>
      <td>187.0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>3.0</td>
      <td>1003.0</td>
      <td>36.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>3.0</td>
      <td>1003.0</td>
      <td>36.0</td>
    </tr>
    <tr>
      <th>20</th>
      <td>71386.0</td>
      <td>1017.0</td>
      <td>470.0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>69721.0</td>
      <td>1006.0</td>
      <td>843.0</td>
    </tr>
  </tbody>
</table>
</div>


