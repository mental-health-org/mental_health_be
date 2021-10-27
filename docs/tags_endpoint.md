# Tag Endpoints

HTTP Verb | Endpoint          | Description
:--------:|-------------------| -----------
GET       | /tags             | Get all tags
GET       | /tags/:id         | Get a single tag

## Get All Tags

Return a list of all tags

`/tags`

### Example Request

`GET https://developer-mental-health-org.herokuapp.com/api/v1/tags`

### Example Response

```
STATUS: 200 OK
```
```
{
    "id": null,
    "type": "tags",
    "attributes": [
        "Depression",
        "First Tag",
        "Second Tag",
        "test",
        "test2",
        "duty to warn",
        "counseling",
        "therapy",
        "law",
        "age of consent",
        "jzxhdjxd"
    ]
}
```

## Get Single Tag

Return a single tag

`/tags/:id`

### Example Request

`GET https://developer-mental-health-org.herokuapp.com/api/v1/tags/2`

### Example Response

```
STATUS: 200 OK
```
```
{
    "id": 2,
    "name": "Depression"
}
```
