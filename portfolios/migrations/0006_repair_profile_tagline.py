from django.db import migrations


def add_tagline_column_if_missing(apps, schema_editor):
    if schema_editor.connection.vendor != 'sqlite':
        return

    cursor = schema_editor.connection.cursor()
    cursor.execute('PRAGMA table_info(portfolios_profile)')
    existing_columns = {row[1] for row in cursor.fetchall()}

    if 'tagline' not in existing_columns:
        cursor.execute(
            "ALTER TABLE portfolios_profile ADD COLUMN tagline varchar(255) NOT NULL DEFAULT ''"
        )


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0005_profile_field_of_study_profile_google_scholar_and_more'),
    ]

    operations = [
        migrations.RunPython(add_tagline_column_if_missing, migrations.RunPython.noop),
    ]
