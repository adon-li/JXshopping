# Generated by Django 3.1.7 on 2021-03-18 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='addrs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to='addrs.addrs', verbose_name='上级行政区划')),
            ],
            options={
                'verbose_name': '省市区',
                'verbose_name_plural': '省市区',
                'db_table': 'tb_addrs',
            },
        ),
    ]