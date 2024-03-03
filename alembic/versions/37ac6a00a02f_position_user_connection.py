"""position_user connection

Revision ID: 37ac6a00a02f
Revises: 3702c680f5d5
Create Date: 2024-03-03 01:20:20.653669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37ac6a00a02f'
down_revision: Union[str, None] = '3702c680f5d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('position_fk', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'user', 'position', ['position_fk'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'position_fk')
    # ### end Alembic commands ###
