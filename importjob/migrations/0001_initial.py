from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ImportJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_key', models.CharField(max_length=40, unique=True)),
                ('endpoint', models.CharField(max_length=80)),
                ('total', models.IntegerField(default=0)),
                ('processed', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('running', 'Running'), ('done', 'Done'), ('failed', 'Failed')], default='running', max_length=10)),
                ('started_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('error', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'importjob',
                'managed': True,
            },
        ),
    ]
