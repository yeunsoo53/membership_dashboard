"""Drop committee table and recreate with autoincrementing committee_id

Revision ID: 55965eb588f1
Revises: b37ecb61c0f5
Create Date: 2025-03-08 10:48:28.281418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '55965eb588f1'
down_revision: Union[str, None] = 'b37ecb61c0f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the existing table
    op.execute("DROP TABLE committee CASCADE")
    
    # Recreate the table with proper auto-increment
    op.create_table('committee',
        sa.Column('committee_id', sa.Integer(), sa.Identity(always=False), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('division', postgresql.ENUM('DEVELOPMENT', 'EXTERNAL', 'INTERNAL', 'OPERATIONS', 
                                        name='committeedivision', create_type=False), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE committee CASCADE")

    op.create_table('committee',
        sa.Column('committee_id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('division', postgresql.ENUM('DEVELOPMENT', 'EXTERNAL', 'INTERNAL', 'OPERATIONS', 
                                        name='committeedivision', create_type=False), nullable=False)
    )
