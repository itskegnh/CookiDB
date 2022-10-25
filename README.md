# CookiDB
A simple open-source NoSQL online database perfect for side projects.

## What is CookiDB?
Created in 2022, CookiDB is a simple online database that is perfect for side projects. It is open-source and free to use. It is also very easy to use, and you can get started in just a few minutes.

## Database API
Endpoint: `http://db.cooki.lol`

### Create Database
**CREATE** `/database`

*Response:*
```json
{
  "database": "DATABASE_ID",
  "token": "AUTH_TOKEN"
}
```

### Delete Database
**DELETE** `/database?id=DATABASE_ID&key=null`

*Headers:*
```
Authorization: AUTH_TOKEN
```

### Read Database
**GET** `/database?id=DATABASE_ID&key=null`

*Headers:*
```
Authorization: AUTH_TOKEN
```

*Response:*
```json
{
    "KEY": "VALUE",
    "ANOTHER_KEY": "ANOTHER_VALUE"
}
```

### Write Database
**PUT** `/database?id=DATABASE_ID`

*Headers:*
```
Authorization: AUTH_TOKEN
```

*Body:*
```json
{
    "KEY": "VALUE",
    "ANOTHER_KEY": "ANOTHER_VALUE"
}
```

### Update Database
**PATCH** `/database?id=DATABASE_ID`

*Headers:*
```
Authorization: AUTH_TOKEN
```

*Body:*
```json
{
    "KEY": "UPDATED_VALUE",
}
```

# GET DATABASE ID AND AUTH TOKEN
[CLICK HERE](http://db.cooki.lol/create) and copy the database ID and auth token.

## Example
```py
import cookidb # /wrappers/cookidb.py

db = cookidb.Database(
    # /create response
    {
        "database": "DATABASE_ID",
        "token": "AUTH_TOKEN"
    }
)

# CLEAR DATABASE
db.clear(key=None)

# READ DATABASE
db.read(key=None)

# WRITE DATABASE
db.write({
    "KEY": "VALUE",
    "ANOTHER_KEY": "ANOTHER_VALUE"
})

# UPDATE DATABASE
db.update({
    "KEY": "UPDATED_VALUE",
})
```