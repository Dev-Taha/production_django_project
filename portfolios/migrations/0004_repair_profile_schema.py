from django.db import migrations


def add_missing_profile_columns(apps, schema_editor):
    if schema_editor.connection.vendor != 'sqlite':
        return

    cursor = schema_editor.connection.cursor()
    cursor.execute('PRAGMA table_info(portfolios_profile)')
    existing_columns = {row[1] for row in cursor.fetchall()}

    def add_column(column_name, ddl):
        if column_name not in existing_columns:
            cursor.execute(ddl)

    add_column('slug', 'ALTER TABLE portfolios_profile ADD COLUMN slug varchar(120)')
    add_column('current_status', 'ALTER TABLE portfolios_profile ADD COLUMN current_status varchar(140)')
    add_column('profile_image', 'ALTER TABLE portfolios_profile ADD COLUMN profile_image varchar(100)')
    add_column('cv_file', 'ALTER TABLE portfolios_profile ADD COLUMN cv_file varchar(100)')
    add_column('theme_id', 'ALTER TABLE portfolios_profile ADD COLUMN theme_id bigint')
    add_column('is_published', 'ALTER TABLE portfolios_profile ADD COLUMN is_published bool DEFAULT 0')

    cursor.execute(
        "UPDATE portfolios_profile SET profile_image = profile_picture WHERE profile_image IS NULL"
    )
    cursor.execute(
        "UPDATE portfolios_profile SET current_status = '' WHERE current_status IS NULL"
    )
    cursor.execute(
        "UPDATE portfolios_profile SET slug = lower(replace(full_name, ' ', '-')) || '-' || id WHERE slug IS NULL OR slug = ''"
    )
    cursor.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS portfolios_profile_slug_uniq ON portfolios_profile(slug)"
    )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0003_profile_research_interests'),
    ]

    operations = [
        migrations.RunPython(add_missing_profile_columns, noop_reverse),
    ]
