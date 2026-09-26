from django.db import migrations, models


class Migration(migrations.Migration):
    # Records the LorryDriver field, which exists in the table but was never
    # in a migration. State only: the real column (varchar(40), a foreign key
    # to lorrydriver) is left exactly as it is. Without this, makemigrations
    # generated an AddField that failed with "Duplicate column".

    dependencies = [
        ('iv', '0013_iv_docno_index_udfbook_docdate_index'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='iv',
                    name='lorrydriver',
                    field=models.CharField(db_column='LorryDriver', max_length=25, null=True),
                ),
            ],
            database_operations=[],
        ),
    ]
