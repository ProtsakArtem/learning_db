"""test migration fake inputs

Revision ID: cc75e8b7c7b5
Revises: 51eafd6456c9
Create Date: 2024-06-21 07:52:39.134620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc75e8b7c7b5'
down_revision: Union[str, None] = '51eafd6456c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
