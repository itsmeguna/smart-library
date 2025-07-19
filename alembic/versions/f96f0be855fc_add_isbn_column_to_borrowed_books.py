"""Add isbn column to borrowed_books

Revision ID: f96f0be855fc
Revises: f694fe7353b7
Create Date: 2025-07-18 12:57:14.378658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f96f0be855fc'
down_revision: Union[str, Sequence[str], None] = 'f694fe7353b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('borrowed_books', sa.Column('isbn', sa.String(), nullable=False))

def downgrade() -> None:
    op.drop_column('borrowed_books', 'isbn')
