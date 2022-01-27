# API
## headers
- `content-type: application/json;`
- `Autentification: Token {token}`

## url variables
- `format=json`


# Captcha
### request
- POST: `/captcha/`

### response
```json
{
    "captcha_key": "type: uuid4",
    "captcha_image": "type: base64 encoded png image",
    "image_type": "image/png",
    "image_decode": "base64"
}
```


# Users
all urls start with `/users`

## create new user
need to solve captcha before create
### request
- POST: `/`
- DATA:
```json
{
    "username": "type: string",
    "password": "type: string",
    "capthca_key": "type: uuid4",
    "capthca_value": "type: string",
    "info": "type: string (optional)"
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
    "username": "type: string",
    "password": "type: string",
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
            "id": "type: int",
            "username": "type: string",
            "info": "type: string",
            "is_stuff": "type: bool",
            "registration_date": "type: date"
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
    "id": "type: int",
    "username": "type: string",
    "info": "type: string",
    "is_stuff": "type: bool",
    "registration_date": "type: date"
}
```

## update user data
### request
- PATCH: `/{user id}/`
- permissions: self or admin
- DATA:
```json
{
    "username": "type: string (optional)",
    "info": "type: string (optional)",
}
```

### response
```json
{
    "id": "type: int",
    "username": "type: string",
    "info": "type: string",
    "is_stuff": "type: bool",
    "registration_date": "type: date"
}
```

## change user password
### request
- PATCH: `/change_password/`
- permissions: authenticated
- DATA:
```json
{
    "old_password": "type: string",
    "new_password": "type: string"
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
