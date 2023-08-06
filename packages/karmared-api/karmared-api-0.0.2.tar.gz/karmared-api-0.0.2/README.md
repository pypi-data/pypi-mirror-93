karmared-api
===============

Install
-------

```
$ pip install karmared-api
```

Use
---

Package contain `Karma` class:

```
from karmared_api import Karma

# create instance, use token
karma = Karma(token)

# or use email and password
karma = await Karma.login(email, password)

query = "{ viewer { id } }"
res = await karma.request(query)
```
