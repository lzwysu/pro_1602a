#coding:utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import logging
from django.conf import settings
from models import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage,InvalidPage
from django.db.models import Count
from django.db import connection
from blog.forms import CommentForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.
log = logging.getLogger('blog.views')

# 全局配置函数
def glb_settings(req):
    SITE_URL = settings.SITE_URL
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    MEDIA_URL = settings.MEDIA_URL
    # 获取分类
    cats = Category.objects.all()
    # 评论排行
    comments = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    comment_article = [Article.objects.get(id=comment['article']) for comment in comments]
    # 点击量排行
    click_article = Article.objects.all().order_by('-click_count')[:2]
    # 站长推荐
    recommend_article = Article.objects.filter(is_recommend=True)[:2]
    # 标签
    tags = Tag.objects.all()
    # 友情链接
    Links = Link.objects.all()
    # 广告 banner
    ads = Ad.objects.all()[:2]

    # 获取归档信息
    # archive = Article.objects.values('date_publish').distinct()
    # 执行原生sql 语句
    # cur = connection.cursor()
    # sql = 'SELECT DISTINCT DATE_FORMAT(`blog_article`.`date_publish`,"%Y-%m") FROM `blog_article` ORDER BY `blog_article`.`date_publish` DESC, `blog_article`.`id` ASC LIMIT 21;'
    # archive = cur.execute(sql)
    # res = cur.fetchall()
    # 扩展objects
    archive = Article.objects.disMon()
    return locals()

# 分页函数
def getPage(req,articles):  # 9条文章  每页显示1条  9页
    pn = req.GET.get('pn',1)
    paginator = Paginator(articles,2) # 第二个参数控制每页记录条数
    try:
        articles = paginator.page(pn)
    except (PageNotAnInteger,EmptyPage,InvalidPage),e:
        articles = paginator.page(1)
    return articles

def index(req):
    try:
        articles = Article.objects.all()
        articles = getPage(req,articles)
    except Exception,e:
        log.error(e)
    return render(req,'blog/index.html',locals())

def category(req):
    try:
        cid = req.GET.get('cid',None)
        articles = Article.objects.filter(category=cid)
        articles = getPage(req,articles)
    except Exception,e:
        log.error(e)
    return render(req,'blog/index.html',locals())

def archive(req):
    try:
        y = req.GET.get('y',None)
        m = req.GET.get('m',None)
        if y and m:
            articles = Article.objects.filter(date_publish__icontains=y + '-' + m)
            articles = getPage(req,articles)
    except Exception,e:
        log.error(e)
    return render(req,'blog/index.html',locals())

def tag(req):
    try:
        tid = req.GET.get('tid',None)
        articles = Article.objects.filter(tag=tid)
        articles = getPage(req,articles)
    except Exception,e:
        log.error(e)
    return render(req,'blog/index.html',locals())

def article(req):
    try:
        aid = req.GET.get('aid',None)
        article = Article.objects.get(id=aid)

        article.click_count = int(article.click_count) + 1 #文章浏览量+1
        article.save()

        #创建评论表单
        comment_form = CommentForm({'author' : req.user.username,'aid':aid})
        # if req.user.is_authenticated() else {'aid':aid}

        #获取评论内容
        comments = article.comment_set.all().order_by('id')
        comment_list = []
        for comment in comments:
            # 添加子评论
            for item in comment_list:
                if not hasattr(item,'chrild'):
                    item.chrild = []
                if comment.pid == item:  # 这是item的一条子评论
                    item.chrild.append(comment)
                    break
            if comment.pid is None: # 添加父级评论
                 comment_list.append(comment)
        print comment_list[0].chrild
    except Exception,e:
        log.error(e)
    return render(req,'blog/article.html',locals())

def comment_post(req):
    comment_form = CommentForm(req.POST)
    if comment_form.is_valid():
        #添加数据库
        author = comment_form.cleaned_data['author']
        comment = comment_form.cleaned_data['comment']
        aid = comment_form.cleaned_data['aid']
        Comment.objects.create(content=comment,user=req.user,article_id=aid)
    else:
        return  HttpResponse(comment_form.errors)
    return HttpResponseRedirect(req.META['HTTP_REFERER'])
    # return HttpResponseRedirect('/article?aid=%s' % aid)

# 登陆
def acc_login(req):
    if req.method == 'GET': # 请求登陆页面 但没有提交信息
        return render(req,'blog/login.html')
    else:
        print req.POST
        username = req.POST.get('username',None) #获取用户名
        password = req.POST.get('password',None) #获取密码
        user = authenticate(username=username,password=password) # 验证用户名和密码
        if user is not None: # 用户存在
            login(req,user) # 执行登陆
            return HttpResponseRedirect(req.POST.get('next','/'))
        else:
            return render(req,'blog/login.html',{'log_err':"用户名或密码错误"})

# 注销
def acc_logout(req):
    logout(req)
    return HttpResponseRedirect(req.META['HTTP_REFERER']) #跳回请求发起页面