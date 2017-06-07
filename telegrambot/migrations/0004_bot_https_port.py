# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegrambot', '0003_auto_20160202_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='https_port',
            field=models.PositiveIntegerField(default=None, help_text='Leave empty if the bot webhook is published at the standard HTTPS port (443).', null=True, verbose_name='Webhook HTTPS port', blank=True),
        ),
    ]
