# Example
You work for a company, who manage an online MMO RPG. You need to create a database structure to represent
player's accounts. The accounts must have the following properties:
Wallet Balance
Bank Balance
and Inventory
```js
STRUCT user;

CREATE user.balance;
CREATE user.balance.wallet 0;
CREATE user.balance.bank 0;

CREATE user.inventory;

COMMIT user; // commit all changes in namespace user
```

The company decides to organise their structure more, move balance and inventory into namespace user.eco.*
```js
STRUCT user;

CREATE user.eco;

MOVE user.balance user.eco.balance;
MOVE user.inventory user.eco.inventory;

COMMIT user; // commit all changes in namespace user
```

Now that the structure is complete, design the workflow of a new user.
```js
INSTANCE user "USER_ID";

SET user.eco.balance.wallet 100;
SET user.eco.balance.bank 1000;

COMMIT user; // commit all changes in namespace user
```

The company decides to add a new property to the user structure, the user's name.
```js
STRUCT user;

CREATE user.name "Unnamed";

COMMIT user; // commit all changes in namespace user
```

This automatically updates all instances of user, and adds the property to all instances.
```js
user.name "Unnamed"
user.eco.balance.wallet 100
user.eco.balance.bank 1000
user.eco.inventory
```

user_id
    name "Unnamed"
    eco
        balance
            wallet 100
            bank 1000
        inventory
