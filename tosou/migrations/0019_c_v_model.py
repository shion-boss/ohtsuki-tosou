# Generated by Django 3.0.7 on 2020-06-18 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tosou', '0018_auto_20200618_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='c_v_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.CharField(blank=True, default='https://res.cloudinary.com/hlbrfvwak/image/upload/v1592166538/gpm3ei8ydcd11j6u4x8z.png', max_length=500, null=True)),
                ('voice', models.TextField(max_length=140)),
            ],
        ),
    ]