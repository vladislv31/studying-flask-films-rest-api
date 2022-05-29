"""empty message

Revision ID: f1d3fad30a7b
Revises: 8fd26ae4e8de
Create Date: 2022-05-27 17:20:08.684802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1d3fad30a7b'
down_revision = '8fd26ae4e8de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('directors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('films',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('premiere_date', sa.Date(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('poster_url', sa.String(length=255), nullable=True),
    sa.Column('director_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['director_id'], ['directors.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('film_genre',
    sa.Column('film_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['film_id'], ['films.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], )
    )
    op.alter_column('roles', 'name',
               existing_type=sa.VARCHAR(length=25),
               nullable=False)
    op.create_unique_constraint(None, 'roles', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'roles', type_='unique')
    op.alter_column('roles', 'name',
               existing_type=sa.VARCHAR(length=25),
               nullable=True)
    op.drop_table('film_genre')
    op.drop_table('films')
    op.drop_table('genres')
    op.drop_table('directors')
    # ### end Alembic commands ###
