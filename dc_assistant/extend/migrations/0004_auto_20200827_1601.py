# Generated by Django 3.0.3 on 2020-08-27 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('extend', '0003_auto_20200817_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggeditem',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='extend_taggeditem_items', to='extend.Tag'),
        ),
    ]