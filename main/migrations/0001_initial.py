# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-29 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='domria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255, unique=True, verbose_name='URL from')),
                ('title', models.CharField(max_length=255, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 ')),
                ('pub_date', models.DateTimeField(editable=False, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f')),
                ('seller_info', models.TextField(blank=True, null=True)),
                ('ext_info', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('created', '\u0441\u043e\u0437\u0434\u0430\u043d'), ('get_seller_info', '\u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0430 \u0438\u043d\u0444\u0430 \u043e \u043f\u0440\u043e\u0434\u0430\u0432\u0446\u0435'), ('get_ext_info', '\u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0430 \u0434\u043e\u043f \u0438\u043d\u0432\u0430'), ('processed', '\u043e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u043d')], default='created', editable=False, max_length=40)),
            ],
            options={
                'verbose_name': 'domria estate',
                'verbose_name_plural': 'domria estate',
            },
        ),
    ]