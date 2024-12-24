# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from learning_logs.models import Topic
from django.shortcuts import get_object_or_404

def register(request):
    """注册新用户"""
    if request.method!= 'POST':
        # 显示空的注册表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录，再重定向到主页
            login(request, new_user)
            return redirect('learning_logs:index')
    # 显示空表单或指出表单无效
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def topics(request):
    if request.user.is_authenticated:
        topics = Topic.objects.filter(owner=request.user)
    else:
        topics = Topic.objects.filter(public=True)
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def new_topic(request):
    if request.method!= 'POST':
        # 显示空的主题创建表单
        form = TopicForm()
    else:
        # 处理填写好的表单
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            # 获取主题公开设置的值
            new_topic.public = bool(request.POST.get('public'))
            new_topic.save()
            return redirect('learning_logs:topics')
    # 显示空表单或指出表单无效
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    # 检查主题是否公开或当前用户是否为主题所有者
    if topic.public or (request.user.is_authenticated and topic.owner == request.user):
        entries = topic.entry_set.order_by('-date_added')
        context = {'topic': topic, 'entries': entries}
        return render(request, 'learning_logs/topic.html', context)
    else:
        return redirect('learning_logs:topics')