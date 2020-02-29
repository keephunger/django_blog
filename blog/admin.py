from django.contrib import admin

# Register your models here.
from blog.models import Article, BlogUser

admin.site.register(Article)
admin.site.register(BlogUser)
