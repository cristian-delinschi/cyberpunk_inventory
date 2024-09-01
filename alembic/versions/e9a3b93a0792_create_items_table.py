"""Create Items Table

Revision ID: e9a3b93a0792
Revises: 
Create Date: 2024-08-29 09:47:18.993593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e9a3b93a0792'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(), unique=True, index=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.String(255), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
    )


def downgrade():
    op.drop_table('items')
