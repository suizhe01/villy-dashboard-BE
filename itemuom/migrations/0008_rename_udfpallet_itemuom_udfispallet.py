from django.db import migrations


class Migration(migrations.Migration):
    # Records a rename made in code without a migration. Both names use the
    # column UdfPallet, so this changes nothing in the database. Without it,
    # makemigrations offered "remove udfpallet + add udfispallet", which would
    # have dropped the column and every pallet flag in it.

    dependencies = [
        ('itemuom', '0007_itemuom_udfpallet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemuom',
            old_name='udfpallet',
            new_name='udfispallet',
        ),
    ]
