"""Add more columns to member table

Revision ID: 3dafe084c9e6
Revises: 421e74be8bd0
Create Date: 2025-03-14 11:07:53.447002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dafe084c9e6'
down_revision: Union[str, None] = '421e74be8bd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member', sa.Column('major', sa.String(length=255), nullable=False))
    op.alter_column('member', 'linkedin',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('member', 'insta',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('member', 'insta',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('member', 'linkedin',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.drop_column('member', 'major')
    # ### end Alembic commands ###
