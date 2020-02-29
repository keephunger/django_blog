import jsonpickle as jsonpickle
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View
from itsdangerous import TimedJSONWebSignatureSerializer

from blog.forms import ArticleModelForm
from blog.models import BlogUser, Article, Comment


# 检查是否登录的装饰器
def login_detection(fun1):
    """
    使用了这个装饰,如果登陆了,此界面就无法访问,直接跳到主页
    :param fun1:
    :return:
    """

    def fun2(*args, **kwargs):
        user = args[0].session.get('user', 0)
        if (user):
            return HttpResponseRedirect(reverse('blog:blog_index'))
        return fun1(*args, **kwargs)

    return fun2


def blog_index(request):
    """
    主页
    :param request:
    :return:
    """
    user = request.session.get('user', 0)
    context = pagenator_articles(request)  # 调用文章分页器
    if (user):
        user = jsonpickle.decode(user)
        context['theuser'] = user

        return render(request, 'index.html', context)
    return render(request, 'index.html', context)


class BlogLogin(View):
    """
    登录
    """

    @staticmethod
    @login_detection
    def get(request):
        return render(request, 'login.html')

    @staticmethod
    def post(request):
        user = BlogUser.objects.filter(username=request.POST.get('username')).first()
        pwd = request.POST.get('pwd')
        if user and user.password == pwd and user.active_flag == 1:
            request.session['user'] = jsonpickle.encode(user)
            return JsonResponse({'flag': 0})
        else:
            return JsonResponse({'flag': -1})


class Register(View):
    """
    注册
    """

    @staticmethod
    @login_detection
    def get(request):
        return render(request, 'register.html')

    @staticmethod
    def post(request):
        from django.core.mail import send_mail
        # 获取信息
        username = request.POST.get('username')
        user = BlogUser.objects.filter(username=username)
        # 加密邮箱验证信息
        t = TimedJSONWebSignatureSerializer('hello你爱你', expires_in=3600)
        res = t.dumps({'user_name': username})
        res = res.decode()
        #获取信息
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        # 如无重复名创建用户
        if len(user) == 0:
            BlogUser.objects.create(username=username, password=pwd, email=email)
        #已激活
        elif user.first().active_flag == 1:
             return JsonResponse({'flag': -1})

        send_mail(
            subject='欢迎注册',
            message="",
            from_email='254414795@qq.com',
            recipient_list=[email],
            fail_silently=False,
            html_message='<a href="https://stormy-brushlands-24614.herokuapp.com/activate/?token={}">点击注册</a>'.format(
                res)
        )

        return HttpResponse('请前往邮箱验证')


def activate(request):
    """
    激活
    :param request:
    :return:
    """
    token = request.GET.get('token')
    t = TimedJSONWebSignatureSerializer('hello你爱你', expires_in=3600)
    user_name = t.loads(token)
    list = BlogUser.objects.filter(username=user_name['user_name'])
    if len(list) == 1:
        list[0].active_flag = 1
        list[0].save()
        return HttpResponseRedirect(reverse('blog:blog_index'))
    return HttpResponse('注册失败')


def logout(request):
    """
    登出
    :param request:
    :return:
    """
    if request.session.get('user', ''):
        del request.session['user']
    return render(request, 'index.html')


def show_article(request):
    """
    展示文章
    :param request:
    :return:
    """
    id = request.GET.get('id', '')
    if not id: return HttpResponse(0)  # 错误
    article = Article.objects.filter(id=id).first()
    if not article: return HttpResponse(0)  # 错误
    article.viewed()  # 增加阅读1
    context = pagenator_comments(request, article)  # 评论分页器
    context["article"] = article
    # 检测是否登录
    user = request.session.get('user', 0)

    # 是否已经登录
    if (user):
        user = jsonpickle.decode(user)
        context["theuser"] = user
        return render(request, 'article.html', context)

    return render(request, 'article.html', context)


class Publish(View):

    @staticmethod
    def get(request):
        # 检测是否登录
        user = request.session.get('user', 0)
        # 是否已经登录
        if (user):
            user = jsonpickle.decode(user)
            form = ArticleModelForm  # 富文本
            return render(request, 'publish_art.html', {'theuser': user, 'form': form})

        return render(request, 'login.html')

    @staticmethod
    def post(request):
        form = ArticleModelForm(request.POST)
        user = jsonpickle.decode(request.session.get('user', ''))
        if form.is_valid():
            form.instance.author = user  # 附上user
            form.save()
            return HttpResponseRedirect(reverse('blog:show_article') + f'?id={form.instance.id}')
        return HttpResponse('faile')


def comment(request):
    """
    发布评论
    :param request:
    :return:
    """
    article_id = request.GET.get('id', '')
    user = request.session.get('user', '')
    if not user : return HttpResponse("请登录,测试用户:18832059218,密码123456")
    user = jsonpickle.decode(user)
    comment = request.POST.get('comment', '')
    if article_id and user and comment:
        article = Article.objects.get(id=article_id)
        Comment.objects.create(user=user.username, content=comment, article=article).save()
        article.commenced()
        return HttpResponseRedirect(reverse('blog:show_article') + f'?id={article_id}')
    else:
        return HttpResponse(0)


def pagenator_articles(request):
    """
    文章分页器
    :param request:
    :return:
    """
    num = request.GET.get('num', '1')
    if num.isdigit():#防止非数字
        num = int(num)
    else:
        num=1
    articles = Article.objects.all()
    paginator = Paginator(articles, 2)
    try:
        article_per_page = paginator.page(num)  # 获取当前页码的记录
    except PageNotAnInteger:  # 如果用户输入的页码不是整数时,显示第1页的内容
        article_per_page = paginator.page(1)
    except EmptyPage:  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        article_per_page = paginator.page(paginator.num_pages)

    # 每页开始页码
    begin = (num - 5)
    if begin < 1:
        begin = 1

    # 每页结束页码
    end = begin + 9
    if end > paginator.num_pages:
        end = paginator.num_pages

    if end <= 10:
        begin = 1
    else:
        begin = end - 9

    pagelist = range(begin, end + 1)
    context = {'article_per_page': article_per_page, 'pagelist': pagelist}
    return context


def pagenator_comments(request, article):
    """
     评论分页器
     :param request:
     :return:
     """
    num = request.GET.get('num', '1')
    if num.isdigit():#防止非数字
        num = int(num)
    else:
        num=1
    comments = Comment.objects.filter(article=article)
    paginator = Paginator(comments, 2)
    try:
        comment_per_page = paginator.page(num)  # 获取当前页码的记录
    except PageNotAnInteger:  # 如果用户输入的页码不是整数时,显示第1页的内容
        comment_per_page = paginator.page(1)
    except EmptyPage:  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        comment_per_page = paginator.page(paginator.num_pages)

    # 每页开始页码
    begin = (num - 5)
    if begin < 1:
        begin = 1

    # 每页结束页码
    end = begin + 9
    if end > paginator.num_pages:
        end = paginator.num_pages

    if end <= 10:
        begin = 1
    else:
        begin = end - 9

    pagelist = range(begin, end + 1)
    context = {'comment_per_page': comment_per_page, 'pagelist': pagelist}
    return context
