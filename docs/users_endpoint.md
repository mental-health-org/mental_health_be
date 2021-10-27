# User Endpoints

HTTP Verb | Endpoint          | Description
:--------:|-------------------| -----------
POST      | /users/       | Create a new user
GET       | /users/:id    | Get a single user
DELETE    | /users/:id/   | Delete a user

## Post a New User

Create a new user

`/users/`

### JSON Payload

Parameter | Data Type      | Required (Y/N) | Default        | Notes  
----------|:--------------:|:--------------:|:-------:       |:------:
username  | String         | Yes            |                |
title     | String         | No             | Null           |

### Example Request

`POST https://developer-mental-health-org.herokuapp.com/api/v1/users/`

### Response Status

```
STATUS: 201 Created
```

## Get Single User

Return a single user and their attributes

`/users/:id`

### Example Request

`GET https://developer-mental-health-org.herokuapp.com/api/v1/users/3`

### Example Response

```
STATUS: 200 OK
```
```
{
    "id": 4,
    "username": "scuba steve",
    "title": "counselor",
    "created_at": "2021-10-25T19:52:44.016116Z",
    "updated_at": "2021-10-25T19:52:59.289063Z"
}
```

## Delete a User

Delete an existing user

`/users/:id/`             

### Example Request

`DELETE https://developer-mental-health-org.herokuapp.com/api/v1/users/3/`

### Response Status

```
STATUS: 204 No Content
```
