"""make_session_word_correct_nullable

Revision ID: 4bd8b90e60b9
Revises: 75a758d9e86e
Create Date: 2025-12-28 10:26:34.487344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bd8b90e60b9'
down_revision: Union[str, Sequence[str], None] = '75a758d9e86e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Make correct column nullable in session_results table
    op.alter_column('session_results', 'correct',
                    existing_type=sa.Boolean(),
                    nullable=True,
                    server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    # Make correct column NOT NULL again
    op.alter_column('session_results', 'correct',
                    existing_type=sa.Boolean(),
                    nullable=False)
