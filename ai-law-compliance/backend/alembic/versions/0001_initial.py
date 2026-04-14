"""initial laws table

Revision ID: 0001_initial
Revises: 
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'laws',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('title', sa.String(512), nullable=False),
        sa.Column('state', sa.String(2), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('full_text', sa.Text(), nullable=True),
        sa.Column('plain_english_summary', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('active', 'pending', 'failed', 'repealed', name='lawstatus'), default='pending'),
        sa.Column('effective_date', sa.String(32), nullable=True),
        sa.Column('ai_category', sa.String(128), nullable=True),
        sa.Column('industries_affected', ARRAY(sa.String()), nullable=True),
        sa.Column('risk_level', sa.Enum('high', 'medium', 'low', name='risklevel'), default='medium'),
        sa.Column('compliance_steps', ARRAY(sa.Text()), nullable=True),
        sa.Column('source_url', sa.String(1024), nullable=True),
        sa.Column('last_updated', sa.DateTime(), nullable=True),
        sa.Column('is_ai_relevant', sa.Boolean(), default=True),
        sa.Column('vector_indexed', sa.Boolean(), default=False),
    )
    op.create_index('ix_laws_state', 'laws', ['state'])
    op.create_index('ix_laws_status', 'laws', ['status'])


def downgrade():
    op.drop_index('ix_laws_status', table_name='laws')
    op.drop_index('ix_laws_state', table_name='laws')
    op.drop_table('laws')
    op.execute("DROP TYPE IF EXISTS lawstatus")
    op.execute("DROP TYPE IF EXISTS risklevel")
