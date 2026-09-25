from django.db import migrations, models


class Migration(migrations.Migration):
    # Adds an index only. The table has an unrecorded LorryDriver column, so
    # this is written by hand to avoid picking that up.

    dependencies = [
        ('cn', '0008_cn_udfbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cn',
            name='docno',
            field=models.CharField(db_column='DocNo', db_index=True, max_length=255),
        ),
    ]
