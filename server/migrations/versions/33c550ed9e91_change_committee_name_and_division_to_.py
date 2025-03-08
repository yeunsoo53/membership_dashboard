"""Change committee name and division to enum types (empty table approach)

Revision ID: 33c550ed9e91
Revises: 196039e5a525
Create Date: 2025-03-07

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33c550ed9e91'
down_revision: Union[str, None] = '196039e5a525'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema by recreating the empty committee table."""
    
    # Drop the existing empty table (with CASCADE to handle dependencies)
    op.execute("DROP TABLE committee CASCADE")
    
    # Create the enum types
    op.execute("""
    CREATE TYPE committeename AS ENUM (
        'CAREER_FAIR', 'CORPORATE', 'ENG_DEV', 'FINANCE', 'PROTRIP',
        'EWEEK', 'ENVISION', 'PHILANTHROPY', 'SPECIAL_EVENTS',
        'LEGISLATION', 'SAGR', 'STUDENT_RELATIONS', 'IR',
        'MARKETING', 'SYSAD', 'MEMBERSHIP'
    )
    """)
    
    op.execute("""
    CREATE TYPE committeedivision AS ENUM (
        'DEVELOPMENT', 'EXTERNAL', 'INTERNAL', 'OPERATIONS'
    )
    """)
    
    # Create the new committee table with enum types
    op.execute("""
    CREATE TABLE committee (
        committee_id INTEGER PRIMARY KEY,
        name committeename NOT NULL,
        division committeedivision NOT NULL
    )
    """)
    
    # Re-create foreign key constraints
    op.execute("""
    ALTER TABLE member_history 
    ADD CONSTRAINT member_history_committee_id_fkey 
    FOREIGN KEY (committee_id) REFERENCES committee (committee_id)
    """)
    
    op.execute("""
    ALTER TABLE committee_activity 
    ADD CONSTRAINT committee_activity_committee_id_fkey 
    FOREIGN KEY (committee_id) REFERENCES committee (committee_id)
    """)
    
    op.execute("""
    ALTER TABLE event 
    ADD CONSTRAINT event_committee_id_fkey 
    FOREIGN KEY (committee_id) REFERENCES committee (committee_id)
    """)


def downgrade() -> None:
    """Downgrade schema back to string columns."""
    
    # Drop the committee table and its constraints
    op.execute("DROP TABLE committee CASCADE")
    
    # Create the committee table with string columns
    op.execute("""
    CREATE TABLE committee (
        committee_id INTEGER PRIMARY KEY,
        name VARCHAR(255),
        division VARCHAR(255)
    )
    """)
    
    # Re-create foreign key constraints
    op.execute("""
    ALTER TABLE member_history 
    ADD CONSTRAINT member_history_committee_id_fkey 
    FOREIGN KEY (committee_id) REFERENCES committee (committee_id)
    """)
    
    op.execute("""
    ALTER TABLE committee_activity 
    ADD CONSTRAINT committee_activity_committee_id_fkey 
    FOREIGN KEY (committee_id) REFERENCES committee (committee_id)
    """)
    
    op.execute("""
    ALTER TABLE event 
    ADD CONSTRAINT event_committee_id_fkey 
    FOREIGN KEY (committee_id) REFERENCES committee (committee_id)
    """)
    
    # Drop the enum types
    op.execute("DROP TYPE IF EXISTS committeename")
    op.execute("DROP TYPE IF EXISTS committeedivision")