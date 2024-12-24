"""added_salt_column

Revision ID: 902037a23b16
Revises: 97a8fc285b42
Create Date: 2024-12-24 13:49:40.803409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '902037a23b16'
down_revision: Union[str, None] = '97a8fc285b42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('email_access', sa.Column('password_salt', sa.LargeBinary(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('email_access', 'password_salt')
    # ### end Alembic commands ###
