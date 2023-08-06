# QLEDA
QLEDA is a python project to read or create schematics and netlists.
The data model uses the popular framework [SQLAlchemy](https://www.sqlalchemy.org/).
Therfore the created data can be stored in either a [PostgreSQL](https://www.postgresql.org/) database or in a 
[SQLite](https://www.sqlite.org/index.html) database.

## Coding Rules
In general [Python Style Guide PEP 8](https://www.python.org/dev/peps/pep-0008/) should be respected.

### SQL Alchemy

#### relationship:
If files are on the same hierarchy (same package) use 'back_populates' wherever possible since it improves code
readability.
If a package/class e.g. 'B' depends on package 'A' but 'A' not on 'B', use 'backref' in order to avoid unnecessary
dependencies.

#### Table names
Table names shall be lowercase of the Class name with an underscore. It's allowed to shorten the name where it makes sense.

### FileStructure
- **common/** TBD
- **core/** all basic functionalities are here
- **drawing/** everything related to graphical representation
- **pypads/** importer function to read library and schemtic data from PADS Logic ascii files.

## Testing
Add unittests in a subfolder named `test`. Name every unittest file `test_` + `file_to_test`.
To run all tests run:
```bash
python -m unittest discover -t ./ -s qleda/
```
from the project base directory.

## Setup
At least Python 3.9 is required.
Install `requirements.txt`.

