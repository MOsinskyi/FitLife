"""add_email_campaigns_table

Revision ID: d52a081d5312
Revises: 073d924cbfcd
Create Date: 2026-05-31 15:39:26.380292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd52a081d5312'
down_revision: Union[str, Sequence[str], None] = '073d924cbfcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'email_campaigns',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('subject', sa.String(), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('frequency', sa.Enum('DAILY', 'WEEKLY', 'MONTHLY', 'ONCE', name='campaignfrequency'), nullable=False),
        sa.Column('send_time', sa.Time(), nullable=False),
        sa.Column('send_day', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('last_sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('email_campaigns')
    sa.Enum(name='campaignfrequency').drop(op.get_bind(), checkfirst=False)
