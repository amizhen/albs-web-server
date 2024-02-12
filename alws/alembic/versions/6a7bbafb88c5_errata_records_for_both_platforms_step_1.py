"""Errata records for both platforms step 1

Revision ID: 6a7bbafb88c5
Revises: 4d128cf0914b
Create Date: 2024-02-12 12:23:48.426799

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6a7bbafb88c5'
down_revision = '4d128cf0914b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'new_errata_records',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('platform_id', sa.Integer(), nullable=False),
        sa.Column('module', sa.Text(), nullable=True),
        sa.Column(
            'release_status',
            postgresql.ENUM(
                'NOT_RELEASED', 'IN_PROGRESS', 'RELEASED', 'FAILED',
                name='erratareleasestatus',
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column('last_release_log', sa.Text(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('solution', sa.Text(), nullable=True),
        sa.Column('freezed', sa.Boolean(), nullable=True),
        sa.Column('issued_date', sa.DateTime(), nullable=False),
        sa.Column('updated_date', sa.DateTime(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('original_description', sa.Text(), nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('oval_title', sa.Text(), nullable=True),
        sa.Column('original_title', sa.Text(), nullable=False),
        sa.Column('contact_mail', sa.Text(), nullable=False),
        sa.Column('status', sa.Text(), nullable=False),
        sa.Column('version', sa.Text(), nullable=False),
        sa.Column('severity', sa.Text(), nullable=False),
        sa.Column('rights', sa.Text(), nullable=False),
        sa.Column('definition_id', sa.Text(), nullable=False),
        sa.Column('definition_version', sa.Text(), nullable=False),
        sa.Column('definition_class', sa.Text(), nullable=False),
        sa.Column('affected_cpe', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('criteria', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('original_criteria', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('tests', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('original_tests', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('objects', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('original_objects', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('states', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('original_states', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('variables', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('original_variables', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(
            ('platform_id',),
            ['platforms.id'],
            name='new_errata_records_platform_id_fkey',
        ),
        sa.PrimaryKeyConstraint('id', 'platform_id')
    )
    op.create_table(
        'new_errata_references',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('href', sa.Text(), nullable=False),
        sa.Column('ref_id', sa.Text(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column(
            'ref_type',
            postgresql.ENUM(
                'cve', 'rhsa', 'self_ref', 'bugzilla',
                name='erratareferencetype', create_type=False
            ),
            nullable=False,
        ),
        sa.Column('errata_record_id', sa.Text(), nullable=True),
        sa.Column('platform_id', sa.Integer(), nullable=True),
        sa.Column('cve_id', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ('cve_id',),
            ['errata_cves.id'],
            name='new_errata_reference_cve_id_fk',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ('errata_record_id', 'platform_id'),
            ['new_errata_records.id', 'new_errata_records.platform_id'],
            name="new_errata_references_errata_record_platform_id_fkey",
        ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'new_errata_packages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('errata_record_id', sa.Text(), nullable=True),
        sa.Column('platform_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('version', sa.Text(), nullable=False),
        sa.Column('release', sa.Text(), nullable=False),
        sa.Column('epoch', sa.Integer(), nullable=False),
        sa.Column('arch', sa.Text(), nullable=False),
        sa.Column('source_srpm', sa.Text(), nullable=True),
        sa.Column('reboot_suggested', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ('errata_record_id', 'platform_id'),
            ['new_errata_records.id', 'new_errata_records.platform_id'],
            name="new_errata_package_errata_record_platform_id_fkey",
        ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'new_errata_to_albs_packages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('errata_package_id', sa.Integer(), nullable=False),
        sa.Column('albs_artifact_id', sa.Integer(), nullable=True),
        sa.Column('pulp_href', sa.Text(), nullable=True),
        sa.Column(
            'status',
            postgresql.ENUM(
                'proposal', 'skipped', 'released', 'approved',
                name='erratapackagestatus',
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('arch', sa.Text(), nullable=False),
        sa.Column('version', sa.Text(), nullable=False),
        sa.Column('release', sa.Text(), nullable=False),
        sa.Column('epoch', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ('albs_artifact_id',),
            ['build_artifacts.id'],
            name='new_errata_to_albs_packages_albs_artifact_id_fkey',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ('errata_package_id',),
            ['new_errata_packages.id'],
            name='new_errata_to_albs_package_errata_package_id_fk',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id')
    )
    op.execute("ALTER sequence new_errata_references_id_seq RESTART WITH 25000")
    op.execute("ALTER sequence new_errata_packages_id_seq RESTART WITH 110000")
    op.execute("ALTER sequence new_errata_to_albs_packages_id_seq RESTART WITH 160000")
    op.execute(
        "INSERT INTO new_errata_records ("
        "id, platform_id, summary, solution, freezed, issued_date, updated_date, description, "
        "original_description, title, original_title, contact_mail, status, version, "
        "severity, rights, definition_id, definition_version, definition_class, "
        "affected_cpe, criteria, original_criteria, tests, original_tests, "
        "objects, original_objects, states, original_states, variables, original_variables, "
        "oval_title, last_release_log, module, release_status) "
        "SELECT id, platform_id, summary, solution, freezed, issued_date, updated_date, "
        "description, original_description, title, original_title, contact_mail, "
        "status, version, severity, rights, definition_id, definition_version, "
        "definition_class, affected_cpe, criteria, original_criteria, "
        "tests, original_tests, objects, original_objects, states, original_states, "
        "variables, original_variables, oval_title, last_release_log, module, release_status "
        "from errata_records"
    )
    op.execute(
        "INSERT into new_errata_packages (id, platform_id, errata_record_id, name, "
        "version, release, epoch, arch, source_srpm, reboot_suggested) "
        "select errata_packages.id, errata_records.platform_id, errata_packages.errata_record_id, "
        "errata_packages.name, errata_packages.version, errata_packages.release, errata_packages.epoch, "
        "errata_packages.arch, errata_packages.source_srpm, errata_packages.reboot_suggested "
        "from errata_packages inner join errata_records on "
        "errata_packages.errata_record_id = errata_records.id"
    )
    op.execute(
        "INSERT into new_errata_references (id, platform_id, errata_record_id, href, ref_id, title, "
        "ref_type, cve_id) select errata_references.id, errata_records.platform_id, "
        "errata_references.errata_record_id, errata_references.href, errata_references.ref_id, "
        "errata_references.title, errata_references.ref_type, errata_references.cve_id "
        "from errata_references inner join errata_records on "
        "errata_references.errata_record_id = errata_records.id"
    )
    op.execute("INSERT into new_errata_to_albs_packages select * from errata_to_albs_packages")
    op.create_index(
        'new_errata_packages_errata_record_id_platform_id_index',
        'new_errata_packages',
        ['errata_record_id', 'platform_id'],
        unique=False,
    )
    op.create_index(
        'new_errata_references_errata_record_id_platform_id_index',
        'new_errata_references',
        ['errata_record_id', 'platform_id'],
        unique=False,
    )
    op.create_index(
        'new_errata_records_id_platform_id_index',
        'new_errata_records',
        ['id', 'platform_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_new_errata_to_albs_packages_errata_package_id'),
        'new_errata_to_albs_packages',
        ['errata_package_id'],
        unique=False,
    )
    op.create_index(
        'idx_new_errata_packages_name_version',
        'errata_packages',
        ['name', 'version'],
        unique=False,
    )
    op.create_index(
        'idx_new_errata_packages_name_version_arch',
        'errata_packages',
        ['name', 'version', 'arch'],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_new_errata_packages_name_version_arch',
                  table_name='errata_packages')
    op.drop_index('idx_new_errata_packages_name_version',
                  table_name='errata_packages')
    op.drop_index(op.f('ix_new_errata_to_albs_packages_errata_package_id'),
                  table_name='new_errata_to_albs_packages')
    op.drop_index('new_errata_packages_errata_record_id_platform_id_index',
                  table_name='new_errata_packages')
    op.drop_index('new_errata_records_id_platform_id_index',
                  table_name='new_errata_records')
    op.drop_index('new_errata_references_errata_record_id_platform_id_index',
                  table_name='new_errata_references')
    op.drop_table('new_errata_to_albs_packages')
    op.drop_table('new_errata_packages')
    op.drop_table('new_errata_references')
    op.drop_table('new_errata_records')
    # ### end Alembic commands ###
