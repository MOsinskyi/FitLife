"""initial

Revision ID: 1d715326f76f
Revises: 45012f688680
Create Date: 2026-04-26 15:32:12.084062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d715326f76f'
down_revision: Union[str, Sequence[str], None] = '45012f688680'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
