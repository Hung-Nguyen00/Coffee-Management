# Generated by Django 3.2 on 2022-04-18 02:56

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('quantity', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('buying_price', models.DecimalField(decimal_places=0, default=0, max_digits=11, null=True)),
                ('status', models.CharField(blank=True, choices=[('Bad', 'Bad'), ('Removed', 'Removed'), ('Good', 'Good'), ('Normal', 'Normal'), ('Maintain', 'Maintain')], max_length=10, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
