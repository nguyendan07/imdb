# Generated by Django 2.2.6 on 2019-10-22 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('plot', models.TextField()),
                ('year', models.PositiveIntegerField()),
                ('rating', models.IntegerField(choices=[(0, 'NR - Not Rated'), (1, 'G - General Audiences'), (2, 'PG - Parental Guidance Suggested'), (3, 'R - Restricted')], default=0)),
                ('runtime', models.PositiveIntegerField()),
                ('website', models.URLField(blank=True)),
            ],
            options={
                'ordering': ('-year', 'title'),
            },
        ),
    ]
