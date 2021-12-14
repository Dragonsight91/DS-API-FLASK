# DS-API endpoint (DEPRECATED)

This API is offline and deprecated due to the website it interfaces with being unavailable.
I only rewrote parts of this API to learn flask.

# Endpoints
```
======    ROOT  ENDPOINT   ======
GET /   This might later respond with a nice Frontend

======  RESULTS ENDPOINTS  ======
POST /results
```


## Placeholders used
- **$user:** _your matriculation number_
- **$passwd:** _the password you use_
- **$name** _a placeholder for some value_
- **[name: $placeholder]** _optional parameter_


## Authentication request object
Any Endpoint that needs authentication will expect a request with `application/json` in the following format:
```json
{
    "id": "$user",
    "passwd": "$password",
    ["year": "$DS-Year"]
}
```

____

## Results Endpoint
The Results endpoint expects a `POST` request with the previously mentioned Authentication Request Object and responds with an empty array if nothing was found, or an array of results, where a result is shown below.

```json 
{
    "exNum": "$exNum",
    "points":{
        "online": "$value",
        "written": "$value"
    }
}
```

