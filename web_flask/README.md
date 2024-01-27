# Flask
This directory contains all our flask backend logic

If you encounter any problems after importing 7-dump.sql, the problem is likely the encoding of the state and city tables

Replace `CHARSET=latin1` with `CHARSET=utf8mb4` to match the database structure
And then reimport the 7-dump.sql again.

Check that it all worked by doing
```sql
HBNB_MYSQL_USER=vagrant HBNB_MYSQL_PWD=vagrant1 HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db python3
```
And in the python console,

`from models import storage`

If all is good during that import, then you are good to go.
