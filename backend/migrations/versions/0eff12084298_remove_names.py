"""Remove names

Revision ID: 0eff12084298
Revises: 1c435216b897
Create Date: 2026-03-21 13:41:40.812956

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = '0eff12084298'
down_revision: str | Sequence[str] | None = '1c435216b897'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
