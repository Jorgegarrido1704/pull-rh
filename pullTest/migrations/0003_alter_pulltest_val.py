# Generated by Django 4.2.13 on 2024-06-14 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pullTest', '0002_alter_pulltest_calibre_alter_pulltest_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pulltest',
            name='val',
            field=models.CharField(default=' ', max_length=80),
        ),
    ]
