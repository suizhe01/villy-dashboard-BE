from django.db import migrations, models


class Migration(migrations.Migration):
    # Adds two indexes only. The table has an unrecorded LorryDriver column, so
    # this is written by hand to avoid picking that up.

    dependencies = [
        ('iv', '0012_alter_iv_udfbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iv',
            name='docno',
            field=models.CharField(db_column='DocNo', db_index=True, max_length=20),
        ),
        migrations.AddIndex(
            model_name='iv',
            index=models.Index(fields=['udfbook', 'docdate'], name='iv_udfbook_docdate_idx'),
        ),
    ]
