"""textures table

Revision ID: 30ac6ed772a5
Revises: 
Create Date: 2021-01-23 22:48:02.808126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30ac6ed772a5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('texture',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('info', sa.String(length=255), nullable=True),
    sa.Column('file', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('texture')
    # ### end Alembic commands ###
