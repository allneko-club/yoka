# Generated by Django 4.2.5 on 2023-10-07 01:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='ステータス名')),
                ('rank', models.PositiveIntegerField(unique=True, verbose_name='表示順')),
            ],
            options={
                'verbose_name': '問い合わせステータス',
                'verbose_name_plural': '問い合わせステータス',
                'ordering': ['rank'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='メールアドレス')),
                ('subject', models.CharField(help_text='50文字以内で入力して下さい。', max_length=50, verbose_name='タイトル')),
                ('message', models.TextField(help_text='1000文字以内で入力して下さい。', max_length=1000, verbose_name='本文')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='問い合わせ日時')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contacts.contactstatus', verbose_name='ステータス')),
            ],
            options={
                'verbose_name': '問い合わせ',
                'verbose_name_plural': '問い合わせ',
                'ordering': ['-id'],
            },
        ),
    ]
