from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_transaction_udfispallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='docno',
            field=models.CharField(db_column='DocNo', db_index=True, max_length=20),
        ),
    ]
