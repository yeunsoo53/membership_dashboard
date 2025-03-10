"""Change committee name to varchar

Revision ID: 50b3939782c3
Revises: 33c550ed9e91
Create Date: 2025-03-07 23:02:46.800064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '50b3939782c3'
down_revision: Union[str, None] = '33c550ed9e91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('committee', 'name',
               existing_type=postgresql.ENUM('CAREER_FAIR', 'CORPORATE', 'ENG_DEV', 'FINANCE', 'PROTRIP', 'EWEEK', 'ENVISION', 'PHILANTHROPY', 'SPECIAL_EVENTS', 'LEGISLATION', 'SAGR', 'STUDENT_RELATIONS', 'IR', 'MARKETING', 'SYSAD', 'MEMBERSHIP', name='committeename'),
               type_=sa.String(length=255),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('committee', 'name',
               existing_type=sa.String(length=255),
               type_=postgresql.ENUM('CAREER_FAIR', 'CORPORATE', 'ENG_DEV', 'FINANCE', 'PROTRIP', 'EWEEK', 'ENVISION', 'PHILANTHROPY', 'SPECIAL_EVENTS', 'LEGISLATION', 'SAGR', 'STUDENT_RELATIONS', 'IR', 'MARKETING', 'SYSAD', 'MEMBERSHIP', name='committeename'),
               existing_nullable=False)
    # ### end Alembic commands ###
