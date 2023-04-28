"""create users and account

Revision ID: f09a92a37aab
Revises: 
Create Date: 2023-04-28 13:07:02.853203

"""
from models import users
from alembic import op
import sqlalchemy as sa
import os
from dotenv import load_dotenv
load_dotenv()

# revision identifiers, used by Alembic.
revision = 'f09a92a37aab'
down_revision = None
branch_labels = None
depends_on = None

ADMIN_USERNAME = str(os.environ.get("ADMIN_USERNAME"))
ADMIN_PASSWORD = str(os.environ.get("ADMIN_PASSWORD"))
ADMIN_EMAIL = str(os.environ.get("ADMIN_EMAIL"))


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('hash_password', sa.String(), nullable=False),
                    sa.Column('is_admin', sa.Boolean(), nullable=True),
                    sa.Column('is_a_star', sa.Boolean(), nullable=True),
                    sa.Column('is_email_verified',
                              sa.Boolean(), nullable=True),
                    sa.Column('joined_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('username')
                    )
    op.create_table('account',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('profile_pic', sa.String(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.bulk_insert(users.Users.__table__, rows=[{
        "username": ADMIN_USERNAME,
        "hash_password": users.Users.generate_hash_password(ADMIN_PASSWORD),
        "email": ADMIN_EMAIL,
        "is_admin": True,
        "is_email_verified": True,
    }])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('account')
    op.drop_table('users')
    # ### end Alembic commands ###
