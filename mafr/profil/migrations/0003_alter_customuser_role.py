# Generated by Django 5.1.1 on 2024-09-25 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0002_alter_talentprofile_specialization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('talent', 'Talent'), ('employer', 'Employer')], max_length=10),
        ),
    ]
