# Alembic database migrations

This project uses [Alembic](https://alembic.sqlalchemy.org/) to manage database migrations. Please see the documentation for more information on how to generate new migrations for each database change.

The preferred approach is to make changes to the [SQLAlchemy models in the `training.models` module](../training/models/), then have Alembic [autogenerate a migration](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) based on those changes. The autogenerate approach supports most [common changes](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect) to the models, but more involved changes will require some manual migration editing.

[Refer to the Alembic documentation](https://alembic.sqlalchemy.org/en/latest/) while creating migrations in order to ensure they are done properly.

In general, each migration (whether an upgrade or downgrade) should preserve existing data as much as possible.
