# Generated by Django 2.0.5 on 2018-06-10 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gene', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='luadciseqtl',
            name='cancer_type',
            field=models.TextField(blank=True),
        ),
    ]