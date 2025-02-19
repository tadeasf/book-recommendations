# book-recommendations

A book recommendation engine combining traditional ML with OpenAI.

## How to use Alembic

Alembic is used for database migrations. Here are the key commands:

### Initial Setup

```bash
# Initialize alembic in your project (run once)
alembic init migrations
Edit alembic.ini to set your database URL:
sqlalchemy.url = postgresql://user:password@localhost:5432/bookdb
```

### Creating and Running Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description of your changes"

# Run all pending migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# View migration history
alembic history

# View current migration version
alembic current
```

### Common Operations
```bash
# Generate a new migration after model changes
alembic revision --autogenerate -m "add user table"

# Preview SQL for next migration
alembic upgrade head --sql

# Mark a migration as complete without running it
alembic stamp head
```

Note: Make sure your database URL is properly configured in `alembic.ini` and your models are properly imported in the migration environment.

