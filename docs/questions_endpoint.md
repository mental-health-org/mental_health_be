# Questions Endpoints

HTTP Verb | Endpoint          | Description
:--------:|-------------------| -----------
GET       | /questions        | Get all questions
POST      | /questions/       | Create a new question
GET       | /questions/:id    | Get a single question
PATCH     | /questions/:id/   | Modify a question
DELETE    | /questions/:id/   | Delete a question
GET       | /search/questions | Find questions with keyword or phrase in title
GET       | /filter/questions | Filter questions by tag name

## Get All Questions

Returns a list of all questions from newest to oldest

`/questions`

### Example Request

`GET https://developer-mental-health-org.herokuapp.com/api/v1/questions`

### Example Response

```
STATUS: 200 OK
```
```
[
    {
        "id": 2,
        "title": "Need Help",
        "body": "Questions about anxiety",
        "user": null,
        "response_count": 3,
        "tagging": [],
        "upvotes": 1,
        "downvotes": 0,
        "created_at": "2021-10-21T21:20:57.757299Z",
        "updated_at": "2021-10-21T21:20:57.757318Z"
    },
    {
        "id": 3,
        "title": "Some sort of title",
        "body": "Some body of information",
        "user": {
            "username": "antonio",
            "title": null
        },
        "response_count": 0,
        "tagging": [
            "First Tag",
            "Second Tag"
        ],
        "upvotes": 1,
        "downvotes": 0,
        "created_at": "2021-10-22T00:24:35.360530Z",
        "updated_at": "2021-10-22T00:24:35.360572Z"
    },
    ...
]
```

## Post a Question

Adds a new question to the list

`/questions/`

### JSON Payload

Parameter | Data Type      | Required (Y/N) | Default        | Notes  |
----------|:--------------:|:--------------:|:-------:       |:------:|
title     | String         | Yes            |                |
tags      | String         | Yes            | [ ]            | value can be blank
body      | String         | No             | Empty string   |     
upvotes   | Integer        | No             | 0              |
downvotes | Integer        | No             | 0              |
user      | String/Integer | No             | Null           | specify user id    


### Example Request

`POST https://developer-mental-health-org.herokuapp.com/api/v1/questions/`

### Response Status

```
STATUS: 201 Created
```

## Get Single Question

Return a single question and its attributes

`/questions/:id`

### Example Request

`GET https://developer-mental-health-org.herokuapp.com/api/v1/questions/3`

### Example Response

```
STATUS: 200 OK
```
```
{
    "id": 3,
    "title": "Some sort of title",
    "body": "Some body of information",
    "user": {
        "username": "antonio",
        "title": null
    },
    "tagging": [
        "First Tag",
        "Second Tag"
    ],
    "responses": [
        {
            "body": "Sample comment.",
            "user": {
                "username": "antonio",
                "title": null
            },
            "upvote": 0,
            "downvote": 1,
            "created_at": "2021-10-23T16:11:05.096515Z"
        },
        {
            "body": "sdfadsgsdfghsdfg",
            "user": null,
            "upvote": 0,
            "downvote": 1,
            "created_at": "2021-10-24T20:09:10.397386Z"
        }
    ],
    "upvotes": 1,
    "downvotes": 0,
    "created_at": "2021-10-22T00:24:35.360530Z",
    "updated_at": "2021-10-22T00:24:35.360572Z"
}
```

## Patch a Question

Modify an existing question

`/questions/:id/`

### JSON Payload

Parameter | Data Type      | Notes  |
----------|:--------------:|:------:
title     | String         |             
body      | String         |               


### Example Request

`PATCH https://developer-mental-health-org.herokuapp.com/api/v1/questions/3/`

### Response Status

```
STATUS: 200 OK
```

## Delete a Question

Delete an existing question

`/questions/:id/`             

### Example Request

`DELETE https://developer-mental-health-org.herokuapp.com/api/v1/questions/3/`

### Response Status

```
STATUS: 204 No Content
```

## Get Questions By Keyword or Phrase

Returns a list of questions with titles that contain the specified keyword or phrase

`/search/questions`

### Query

Parameter | Value             | Notes
----------|:-----------------:|:----:
search    | keyword or phrase | case insensitive               

### Example Request

`GET https://developer-mental-health-org.herokuapp.com/api/v1/search/questions?search=need`

### Example Response

```
STATUS: 200 OK
```
```
[
    {
        "id": 2,
        "title": "Need Help",
        "body": "Questions about anxiety",
        "user": null,
        "response_count": 3,
        "tagging": [],
        "upvotes": 1,
        "downvotes": 0,
        "created_at": "2021-10-21T21:20:57.757299Z",
        "updated_at": "2021-10-21T21:20:57.757318Z"
    }
]
```

## Get Questions By Tag Name

Returns a list of questions associated with the specified tag

`/filter/questions`

### Query

Parameter | Value             | Notes
----------|:-----------------:|:----:
tags      | Exact             | case sensitive               

### Example Request

`GET https://developer-mental-health-org.herokuapp.com/api/v1/search/questions?search=First_Tag`

### Example Response

```
STATUS: 200 OK
```
```
[
      {
          "id": 3,
          "title": "Some sort of title",
          "body": "Some body of information",
          "user": {
              "username": "antonio",
              "title": null
          },
          "response_count": 0,
          "tagging": [
              "First Tag",
              "Second Tag"
          ],
          "upvotes": 1,
          "downvotes": 0,
          "created_at": "2021-10-22T00:24:35.360530Z",
          "updated_at": "2021-10-22T00:24:35.360572Z"
      }
]
```
