from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CommissionRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('running', 'Running'), ('done', 'Done'), ('cancelled', 'Cancelled'), ('failed', 'Failed')], default='running', max_length=10)),
                ('cancel_requested', models.BooleanField(default=False)),
                ('started_at', models.DateTimeField()),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('step_timings', models.TextField(blank=True, null=True)),
                ('error', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'commissionrun',
                'managed': True,
            },
        ),
    ]
