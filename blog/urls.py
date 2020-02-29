
from django.contrib import admin
from django.urls import path

from blog import views
app_name="blog"

urlpatterns = [
    path(r'',views.blog_index,name="blog_index"),
    path(r'login/',views.BlogLogin.as_view(),name="blog_login"),#登录
    path(r'register/',views.Register.as_view(),name="blog_register"),#注册
    path(r'logout/', views.logout, name="blog_logout"),#注销
    path(r'activate/',views.activate),#邮箱激活
    path(r'publish/',views.Publish.as_view(),name='publish'),#发布文章
    path(r'article/', views.show_article,name='show_article'),#阅览文章
    path(r'comment/', views.comment, name='blog_comment'),  # 阅览文章
]
