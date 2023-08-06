# simpleurllib3
Easy to use urllib3 simplifier.
Usage:
```
>>> client = simpleurllib3.Client()
>>> resp = client.get('http://httpbin.org/ip')
>>> resp.status
200
>>> resp.data
"{'origin': '127.0.0.1'}"
```

## `class` Client()
PoolManager client.

## `class` SSLClient()
Secure SSL PoolManager client.

## Any Client || Request
```
client.[method](url, args)
```
Returns `urllib3.response.HTTPResponse`,
refer to urllib3 docs for more info.