"""Add enum values to position level. Delete is_coordinator

Revision ID: d9a0e6ecb21e
Revises: 55965eb588f1
Create Date: 2025-03-08 11:15:55.566755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9a0e6ecb21e'
down_revision: Union[str, None] = '55965eb588f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE positionlevel AS ENUM ('GC', 'EC', 'EB')")

    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE position ALTER COLUMN level TYPE positionlevel USING level::positionlevel")
       
    op.drop_column('position', 'is_coordinator')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('position', sa.Column('is_coordinator', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # Convert enum to varchar using USING clause
    op.execute("ALTER TABLE position ALTER COLUMN level TYPE VARCHAR(255) USING level::text")
    
    op.execute("DROP TYPE positionlevel")
