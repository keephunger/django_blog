# Generated by Django 2.2.10 on 2020-02-28 18:36

from django.db import migrations, models
import django.db.models.deletion
import extra_apps.DjangoUeditor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='博客标题')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='日期')),
                ('content', extra_apps.DjangoUeditor.models.UEditorField(blank=True, null=True, verbose_name='内容')),
                ('view', models.BigIntegerField(default=0, verbose_name='阅读数')),
                ('comment_value', models.BigIntegerField(default=0, verbose_name='评论数')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ['-date_time'],
            },
        ),
        migrations.CreateModel(
            name='BlogUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='名字')),
                ('password', models.CharField(max_length=45, verbose_name='密码')),
                ('email', models.CharField(max_length=45, verbose_name='邮箱')),
                ('active_flag', models.IntegerField(default=0, verbose_name='激活标志')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'blog_user',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200, verbose_name='评论内容')),
                ('user', models.CharField(max_length=200, verbose_name='发布者')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='日期')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article', verbose_name='文章')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.BlogUser', verbose_name='作者'),
        ),
    ]
