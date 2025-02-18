#!/bin/bash
set -e

# Apply all pending migrations
alembic upgrade head
