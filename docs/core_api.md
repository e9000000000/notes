# API
## headers
- `content-type: application/json;`
- `Autentification: Token {token}`


## url variables
- `format=json`


# Users
all urls start with `/users`

## create new user
### request
- POST: `/`
- DATA:
```json
{
    "username": "string",
    "password": "string",
    "info": "string (optional)"
}
```

### response
```json
{"success": 1}
```

## get auth token
### request
- POST: `/auth/`
- DATA:
```json
{
    "username": "string",
    "password": "string",
}
```

### response
```json
{"token": string}
```

## delete auth token (make token invalid)
### request
- DELETE: `/auth/`
- permissions: authenticated

### response
```json
{"success": 1}
```

## get users list
### request
- GET:  `/`
#### params
- `page` - page number

### response
```json
{
    "count": "int",
    "next": "url to next page or null",
    "previous": "url to previous page or null",
    "results": [
        {
            "id": "int",
            "username": "string",
            "info": "string",
            "is_stuff": "bool",
            "registration_date": "date"
        },
        ...
    ]
}
```

## get user details
### request
- GET: `/{user id}/`

### response
```json
{
    "id": "int",
    "username": "string",
    "info": "string",
    "is_stuff": "bool",
    "registration_date": "date"
}
```

## update user data
### request
- PATCH: `/{user id}/`
- permissions: self or admin
- DATA:
```json
{
    "username": "string (optional)",
    "info": "string (optional)",
}
```

### response
```json
{
    "id": "int",
    "username": "string",
    "info": "string",
    "is_stuff": "bool",
    "registration_date": "date"
}
```

## change user password
### request
- PATCH: `/change_password/`
- permissions: authenticated
- DATA:
```json
{
    "old_password": "string",
    "new_password": "string"
}
```

### response
```json
{"success": 1}
```

### extra
if `old_password` is wrong, will be http auth error `401`

## delete user
### request
- DELETE: `/{user id}/`
- permissions: self or admin

### response
```json
{"success": 1}
```
