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