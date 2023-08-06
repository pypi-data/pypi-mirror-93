# api functions

This api functions written by python

## Configuration

- Setup as **OS environment variable** with **PY\_** prefix
  - Replace **[]** with your value

```
PY_API_HTTP=[https|http]
PY_API_HOST=[apihost]
PY_API_PORT=[443|80]
PY_API_DATA=[/api/v1/data]
PY_API_USR=[apiuser]
PY_API_PWD=[apipwd]
```

- Setup as ./conf/system.json
  - Replace **[]** with your value

```
{
    "api_http": "[https|http]",
    "api_host": "[apihost]",
    "api_port": "[443|80]",
    "api_data": "[/api/v1/data]",
    "api_usr": "[apiuser]",
    "api_pwd": "[apipwd]"
}
```

## Dependancies

Read more [requirements.txt](./requirements.txt)
