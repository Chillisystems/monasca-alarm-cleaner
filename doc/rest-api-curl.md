
# Access Monasca REST api with curl

#### Fetch Keystone token
```
export TOKEN=`curl -i \
  -H "Content-Type: application/json" \
  -d '
{ "auth": {
    "identity": {
      "methods": ["password"],
      "password": {
        "user": {
          "name": "admin",
          "domain": { "id": "default" },
          "password": "adminpass"
        }
      }
    },
    "scope": {
      "project": {
        "name": "service",
        "domain": { "id": "default" }
      }
    }
  }
}' \
  http://openstack-api:5000/v3/auth/tokens -sS | grep X-Subject-Token |cut -d':' -f 2`
```

#### List monasca alarm definitions

```
curl -i -X GET -H 'X-Auth-User: admin' -H "X-Auth-Token: $TOKEN" -H 'Accept: application/json' -H 'Content-Type: application/json' -H 'X-Auth-Url: http://openstack-api:35357/v3' http://monasca-api-1:8070/v2.0/alarms
```

# INFO

https://adam.younglogic.com/2013/09/keystone-v3-api-examples/
https://github.com/openstack/monasca-api/blob/master/docs/monasca-api-spec.md
http://docs.openstack.org/developer/keystone/api_curl_examples.html