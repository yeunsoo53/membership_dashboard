"""Add location column to meeting table

Revision ID: dc8e527bd4ab
Revises: d9a0e6ecb21e
Create Date: 2025-03-08 12:36:53.063078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc8e527bd4ab'
down_revision: Union[str, None] = 'd9a0e6ecb21e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'committee_activity', 'committee', ['committee_id'], ['committee_id'])
    op.create_foreign_key(None, 'event', 'committee', ['committee_id'], ['committee_id'])
    op.add_column('meeting', sa.Column('location', sa.String(length=255), nullable=False))
    op.create_foreign_key(None, 'member_history', 'committee', ['committee_id'], ['committee_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'member_history', type_='foreignkey')
    op.drop_column('meeting', 'location')
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.drop_constraint(None, 'committee_activity', type_='foreignkey')

    # ### end Alembic commands ###
