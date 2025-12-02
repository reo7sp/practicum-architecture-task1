import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField()),
                ('name', models.CharField(max_length=255)),
                ('scenario', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'scenarios',
            },
        ),
        migrations.AddIndex(
            model_name='scenario',
            index=models.Index(fields=['user_id'], name='scenarios_user_id_idx'),
        ),
    ]
