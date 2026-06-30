from django.db import migrations


def add_missing_profile_columns(apps, schema_editor):
    if schema_editor.connection.vendor != 'sqlite':
        return

    cursor = schema_editor.connection.cursor()
    cursor.execute('PRAGMA table_info(portfolios_profile)')
    existing_columns = {row[1] for row in cursor.fetchall()}

    columns_to_add = [
        ('tagline', 'varchar(255) NOT NULL DEFAULT '''''),
        ('current_status', 'varchar(140) NOT NULL DEFAULT '''''),
        ('profile_image', 'varchar(100) NULL'),
        ('cv_file', 'varchar(100) NULL'),
        ('google_scholar', 'varchar(200) NULL'),
        ('research_gate', 'varchar(200) NULL'),
        ('years_teaching', 'integer NULL'),
        ('citation_count', 'integer NULL'),
        ('students_supervised', 'integer NULL'),
        ('theme_id', 'bigint NULL'),
        ('is_published', 'bool NOT NULL DEFAULT 0'),
        ('selected_template', 'varchar(50) NULL'),
        ('research_interests', 'text NOT NULL DEFAULT '''''),
        ('slug', 'varchar(120) NOT NULL DEFAULT '''''),
    ]

    for name, ddl in columns_to_add:
        if name not in existing_columns:
            cursor.execute(f'ALTER TABLE portfolios_profile ADD COLUMN {name} {ddl}')

    cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS portfolios_profile_slug_uniq ON portfolios_profile(slug)')


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0006_repair_profile_tagline'),
    ]

    operations = [
        migrations.RunPython(add_missing_profile_columns, migrations.RunPython.noop),
    ]
