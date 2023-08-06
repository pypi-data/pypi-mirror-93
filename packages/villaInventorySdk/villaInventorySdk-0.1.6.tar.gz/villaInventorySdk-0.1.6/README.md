# villaInventorySdk



full docs here https://thanakijwanavit.github.io/villa-inventory-sdk/

## Install

`pip install villaInventorySdk`

## How to use

Uploading a large amount of data

## sample input

```
from villaInventorySdk.inventory import InventorySdk
from random import randrange
import boto3, time, json
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
import pandas as pd
from nicHelper.dictUtil import printDict
```

```
sampleInput =  [ 
  { 'iprcode': '0000009', 'brcode': '1000', 'ib_cf_qty': '50', 'new_ib_vs_stock_cv': '27' },
  { 'iprcode': '0000004', 'brcode': '1000', 'ib_cf_qty': '35', 'new_ib_vs_stock_cv': '33' },
  { 'iprcode': '0000003', 'brcode': '1003', 'ib_cf_qty': '36', 'new_ib_vs_stock_cv': '33' }
    ]
df = pd.DataFrame(sampleInput)
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
      <th>iprcode</th>
      <th>brcode</th>
      <th>ib_cf_qty</th>
      <th>new_ib_vs_stock_cv</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0000009</td>
      <td>1000</td>
      <td>50</td>
      <td>27</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0000004</td>
      <td>1000</td>
      <td>35</td>
      <td>33</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0000003</td>
      <td>1003</td>
      <td>36</td>
      <td>33</td>
    </tr>
  </tbody>
</table>
</div>



## Upload data

## init sdk

```
%%time
USER=None
PW = None
sdk = InventorySdk(user=USER, pw=PW, branchName = branch)
```

    CPU times: user 34.2 ms, sys: 7.54 ms, total: 41.8 ms
    Wall time: 40.8 ms


## Update inventory 

```
%%time
key = 'test'
r = sdk.uploadDf(df, key = key)
if r.status_code >= 400: raise Exception(r.json())
sdk.ingestData(key = key)
```

    signed url is 
    url : https://in
    fields
     key : test
     AWSAccessKeyId : ASIAVX4Z5T
     x-amz-security-token : IQoJb3JpZ2
     policy : eyJleHBpcm
     signature : apy2TqqnY2
    CPU times: user 54.7 ms, sys: 12.3 ms, total: 67 ms
    Wall time: 628 ms





    {'body': '{"iprcode":{"0":"0000009","1":"0000004","2":"0000003"},"brcode":{"0":"1000","1":"1000","2":"1003"},"ib_cf_qty":{"0":"50","1":"35","2":"36"},"new_ib_vs_stock_cv":{"0":"27","1":"33","2":"33"}}',
     'statusCode': 200,
     'headers': {'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': '*'}}



#### test uploading full data 

```
#### test uploading real data 
# df = pd.read_csv('sampleData/inventory.csv', index_col=0, dtype=str).reset_index(drop=True)
# r = sdk.uploadDf(df, key = key)
# if r.status_code >= 400: raise Exception(r.json())
# sdk.ingestData(key = key)
```

## Query single product

```
%%time
sdk.querySingleProduct2(iprcode='1234')
```

    succesfully get url, returning pandas
    CPU times: user 103 ms, sys: 12.6 ms, total: 116 ms
    Wall time: 799 ms





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
      <th>iprcode</th>
      <th>brcode</th>
      <th>ib_cf_qty</th>
      <th>new_ib_vs_stock_cv</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>



## Query Branch

```
%%time
sdk.branchQuery(brcode='1000', iprcodes = [9])
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <timed eval> in <module>


    ~/SageMaker/.persisted_conda/python38/lib/python3.8/site-packages/nicHelper/wrappers.py in wrapper(self, *args, **kwargs)
         12         @wraps(func)
         13         def wrapper(self, *args, **kwargs):
    ---> 14             return func(self, *args, **kwargs)
         15         setattr(cls, func.__name__, wrapper)
         16         # Note we are not binding func, but wrapper which accepts self but does exactly the same as func


    TypeError: branchQuery() got an unexpected keyword argument 'iprcodes'


## Query All

```
%%time
sdk.queryAll2()
```

    succesfully get url, returning pandas
    CPU times: user 76.2 ms, sys: 24.1 ms, total: 100 ms
    Wall time: 673 ms





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
      <th>iprcode</th>
      <th>brcode</th>
      <th>ib_cf_qty</th>
      <th>new_ib_vs_stock_cv</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4</td>
      <td>1000</td>
      <td>35</td>
      <td>33</td>
    </tr>
    <tr>
      <th>1</th>
      <td>9</td>
      <td>1000</td>
      <td>95</td>
      <td>95</td>
    </tr>
    <tr>
      <th>2</th>
      <td>12</td>
      <td>1000</td>
      <td>36</td>
      <td>36</td>
    </tr>
    <tr>
      <th>3</th>
      <td>26</td>
      <td>1000</td>
      <td>28</td>
      <td>28</td>
    </tr>
    <tr>
      <th>4</th>
      <td>28</td>
      <td>1000</td>
      <td>9</td>
      <td>9</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>81551</th>
      <td>244818</td>
      <td>1000</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>81552</th>
      <td>244820</td>
      <td>1000</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>81553</th>
      <td>244822</td>
      <td>1000</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>81554</th>
      <td>244823</td>
      <td>1000</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>81555</th>
      <td>3</td>
      <td>1003</td>
      <td>36</td>
      <td>33</td>
    </tr>
  </tbody>
</table>
<p>81556 rows × 4 columns</p>
</div>



```
sdk.querySingleProduct2()
```

    succesfully get url, returning pandas





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
      <th>iprcode</th>
      <th>brcode</th>
      <th>ib_cf_qty</th>
      <th>new_ib_vs_stock_cv</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>


