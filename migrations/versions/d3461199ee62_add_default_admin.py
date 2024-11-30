"""Add default admin

Revision ID: d3461199ee62
Revises: a0c1a649cc01
Create Date: 2024-11-30 13:21:15.647561

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String
from werkzeug.security import generate_password_hash


# revision identifiers, used by Alembic.
revision = 'd3461199ee62'
down_revision = 'a0c1a649cc01'
branch_labels = None
depends_on = None


def upgrade():
    admin_table = table(
        'admins',
        column('id', sa.Integer),
        column('username', sa.String),
        column('password_hash', sa.String)
    )

    op.bulk_insert(
        admin_table,
        [
            {
                'id': 1,
                'username': 'admin',
                'password_hash': generate_password_hash('123')
            }
        ]
    )


def downgrade():
    op.execute("DELETE FROM admins WHERE username = 'admin'")
