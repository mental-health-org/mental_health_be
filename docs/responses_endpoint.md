# Response Endpoints

HTTP Verb | Endpoint          | Description
:--------:|-------------------| -----------
POST      | /responses/       | Post a response to a question
PATCH     | /responses/:id/   | Modify a response
DELETE    | /responses/:id/   | Delete a response

## Post a Response

Adds a response to a question

`/responses/`

### JSON Payload

Parameter | Data Type      | Required (Y/N) | Default        | Notes  |
----------|:--------------:|:--------------:|:-------:       |:------:|
post      | String/Integer | Yes            |                | specify post id
body      | String         | Yes            | Empty string   |     
upvotes   | Integer        | No             | 0              |
downvotes | Integer        | No             | 0              |
user      | String/Integer | No             | Null           | specify user id    


### Example Request

`POST https://developer-mental-health-org.herokuapp.com/api/v1/responses/`

### Response Status

```
STATUS: 201 Created
```

## Patch a Response

Modify an existing response

`/responses/:id/`

### JSON Payload

Parameter | Data Type      | Notes  
----------|:--------------:|:------:
body      | String         |               


### Example Request

`PATCH https://developer-mental-health-org.herokuapp.com/api/v1/responses/3/`

### Response Status

```
STATUS: 200 OK
```

## Delete a Response

Delete an existing response

`/responses/:id/`             

### Example Request

`DELETE https://developer-mental-health-org.herokuapp.com/api/v1/responses/3/`

### Response Status

```
STATUS: 204 No Content
```
