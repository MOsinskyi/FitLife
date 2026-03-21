"""Add created_at and updated_on fields

Revision ID: 90ac2e7d759b
Revises: 0eff12084298
Create Date: 2026-03-21 14:59:44.223953

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = '90ac2e7d759b'
down_revision: str | Sequence[str] | None = '0eff12084298'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
