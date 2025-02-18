#!/bin/bash
set -e

# Create a new migration
alembic revision --autogenerate -m "$1"
