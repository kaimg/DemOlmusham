"""Initial migration

Revision ID: 5aee174663f3
Revises: 
Create Date: 2024-06-17 08:26:17.347873

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5aee174663f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('video',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('video', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_video_timestamp'), ['timestamp'], unique=False)

    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=500), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('video_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['video.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_comment_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.drop_index('idx_comments_timestamp')

    op.drop_table('comments')
    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.drop_index('idx_videos_timestamp')

    op.drop_table('videos')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    sa.UniqueConstraint('username', name='users_username_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('videos',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('videos_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=140), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('url', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='videos_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='videos_pkey'),
    postgresql_ignore_search_path=False
    )
    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.create_index('idx_videos_timestamp', ['timestamp'], unique=False)

    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('body', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('video_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='comments_user_id_fkey'),
    sa.ForeignKeyConstraint(['video_id'], ['videos.id'], name='comments_video_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='comments_pkey')
    )
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.create_index('idx_comments_timestamp', ['timestamp'], unique=False)

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_comment_timestamp'))

    op.drop_table('comment')
    with op.batch_alter_table('video', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_video_timestamp'))

    op.drop_table('video')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
