# usql_conf
Command-Line Tool for Managing SQL Connection Strings.

## Install

```console
pip install git+https://github.com/jpy-git/usql_conf.git
```

## Usage

Create .usql_conf file in home directory and add config names with associated connection strings in .ini format.
e.g.
```
[pg_test]
connection_string = pg://test_user:password123@localhost/test_database?sslmode=disable
```

Then obtain connection string from .usql_conf by running:
```console
usql_conf pg_test
```

The intended usage is to be passed to usql to connect to the desired database:
```console
usql $(usql_conf pg_test)
```
