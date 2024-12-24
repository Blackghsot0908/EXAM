"""定义 learning_logs 的 URL 模式"""
from django.urls import path
from . import views
app_name = 'learning_logs'
urlpatterns = [
# 主页
    path('', views.index, name='index'),

    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    
]