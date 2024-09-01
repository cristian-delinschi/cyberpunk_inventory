"""Create User Table

Revision ID: 670649d93ce8
Revises: e9a3b93a0792
Create Date: 2024-08-29 13:17:52.453753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '670649d93ce8'
down_revision: Union[str, None] = 'e9a3b93a0792'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('email'),
        sa.Index('ix_users_id', 'id')
    )


def downgrade():
    op.drop_table('users')
