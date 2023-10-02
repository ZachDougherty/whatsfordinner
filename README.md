# __Whatsfordinner?__
A website for managing your favorite recipes in one place!

# __Running the app__
This application consists of a flask app and postgres database

## __Requirements__
### __Database__
You'll need a `pg_ctl` and `psql` installed for database setup. Once that's done, start the database with

```sh
make startdb
```

Once the database is running, migrate the database up 1 version with

```sh
make migrate-up
```

If you need to migrate down, run

```sh
make migrate-down
```

This will drop all tables and data in the `whatsfordinner` database, created during `make migrate-up`.

### __Flask__
With the database migrated, run

```sh
make serve
```

This starts the `flask` application at `0.0.0.0:8000`
