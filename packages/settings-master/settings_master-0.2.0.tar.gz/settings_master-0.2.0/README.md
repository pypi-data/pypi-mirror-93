
This Is Package for fast use SETTINGS.

## Example
#### STRUCTURE

```
settings
|
-- db.py
|
-- api.py
|
-- __init__.py
```

#### settings/db.py
```python
DB_NAME = "name"
DB_PASSWORD = "password"
``` 
#### settings/api.py
```python
API_TOKEN = "dekejfire"
```

#### settings/\_\_init__.py
```python

from settings_master import DirectorySettings, settings as this


settings = DirectorySettings(this)
```

Now we can use this:
```python
from settings_master.settings import settings

assert settings.DB_NAME == "name"
assert settings.DB_PASWORD == "password"
assert settings.API_TOKEN == "dekejfire"
```

## DEV
### LINUX / MAC X
```shell script
python3 setup.py sdist upload
twine upload dist/*

```
### WINDOWS
```shell script
python setup.py sdist upload
twine upload dist/*

```
