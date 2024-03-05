"""delete assoc table

Revision ID: f77ffa90bc45
Revises: aa6c42a7d3f3
Create Date: 2024-03-05 18:45:59.130343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f77ffa90bc45'
down_revision: Union[str, None] = 'aa6c42a7d3f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timelog_project_association_table')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timelog_project_association_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timelog_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['timelog_id'], ['timelog.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('timelog_id', 'project_id', name='idx_unique_timelog_project')
    )
    # ### end Alembic commands ###
