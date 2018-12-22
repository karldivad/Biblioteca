# Generated by Django 2.1.4 on 2018-12-22 15:47

import core.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', djongo.models.fields.EmbeddedModelField(model_container=core.models.BookContent, null=True)),
            ],
        ),
    ]
