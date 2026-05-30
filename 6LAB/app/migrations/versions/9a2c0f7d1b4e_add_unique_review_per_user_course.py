"""Add unique review per user and course

Revision ID: 9a2c0f7d1b4e
Revises: 0064961051ef
Create Date: 2026-05-30 10:05:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '9a2c0f7d1b4e'
down_revision = '0064961051ef'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        DELETE FROM reviews
        WHERE id NOT IN (
            SELECT id FROM (
                SELECT MIN(id) AS id
                FROM reviews
                GROUP BY course_id, user_id
            ) AS kept_reviews
        )
    """)
    op.execute("""
        UPDATE courses
        SET rating_sum = COALESCE((
                SELECT SUM(reviews.rating)
                FROM reviews
                WHERE reviews.course_id = courses.id
            ), 0),
            rating_num = COALESCE((
                SELECT COUNT(reviews.id)
                FROM reviews
                WHERE reviews.course_id = courses.id
            ), 0)
    """)

    with op.batch_alter_table('reviews') as batch_op:
        batch_op.create_unique_constraint(
            'uq_reviews_course_id_user_id',
            ['course_id', 'user_id']
        )


def downgrade():
    with op.batch_alter_table('reviews') as batch_op:
        batch_op.drop_constraint('uq_reviews_course_id_user_id', type_='unique')
