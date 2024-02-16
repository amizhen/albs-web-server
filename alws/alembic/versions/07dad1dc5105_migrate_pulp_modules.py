"""Migrate Pulp modules

Revision ID: 07dad1dc5105
Revises: 79b5458320de
Create Date: 2024-02-02 16:17:33.965562

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '07dad1dc5105'
down_revision = '79b5458320de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'build_tasks_rpm_modules_mapping',
        sa.Column('build_task_id', sa.Integer(), nullable=False),
        sa.Column('rpm_module_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['build_task_id'],
            ['build_tasks.id'],
            name="build_tasks_rpm_modules_mapping_build_task_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ['rpm_module_id'],
            ['rpm_module.id'],
            name="build_tasks_rpm_modules_mapping_rpm_module_id_fkey",
        ),
        sa.PrimaryKeyConstraint('build_task_id', 'rpm_module_id'),
    )
    op.execute(
        sa.text(
            "INSERT INTO build_tasks_rpm_modules_mapping (build_task_id, rpm_module_id) "
            "SELECT DISTINCT id, rpm_module_id FROM build_tasks "
            "WHERE rpm_module_id IS NOT NULL"
        )
    )
    op.drop_constraint(
        'build_tasks_rpm_module_id_fkey', 'build_tasks', type_='foreignkey'
    )
    op.drop_column('build_tasks', 'rpm_module_id')
    op.drop_column('rpm_module', 'sha256')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'rpm_module',
        sa.Column(
            'sha256', sa.VARCHAR(length=64), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        'build_tasks',
        sa.Column(
            'rpm_module_id', sa.INTEGER(), autoincrement=False, nullable=True
        ),
    )
    op.create_foreign_key(
        'build_tasks_rpm_module_id_fkey',
        'build_tasks',
        'rpm_module',
        ['rpm_module_id'],
        ['id'],
    )
    op.drop_table('build_tasks_rpm_modules_mapping')
    # ### end Alembic commands ###
