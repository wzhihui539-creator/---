"""day16 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # C老师给了新的内容，neme="给前面的链接起个名"
    path('depart/list/', views.depart_list, name="depart_list"),
    path('depart/add/', views.depart_add, name="depart_add"),
    # <int:nid> 要求一定是数字，并给拿到的数字取个变量名nid，传到views相对应的模块里
    path('depart/<int:nid>/delete/', views.depart_delete, name="depart_delete"),
    # <int:nid>：路径转换器，匹配整数类型的参数并命名为nid（nid 是自定义参数名）；
    # - /delete/：固定 URL 片段，匹配字面量 "/delete/"；
    # 示例：匹配 depart/123/delete/，并将123以nid=123传给视图。
    # 视图函数depart_delete需要接收nid参数（通常定义为def depart_delete(request, nid):），才能获取 URL 中的整数参数；
    path('depart/<int:nid>/edit/', views.depart_edit, name="depart_edit"),
    path('user/list/', views.user_list, name='user_list'),
    path('user/add/', views.user_add, name='user_add'),
    path('user/model/form/add/', views.user_model_form_add, name="model_form_user_add"),
    path('user/<int:nid>/edit/', views.user_edit, name="user_edit"),
    path('user/<int:nid>/delete/', views.user_delete, name="user_delete"),
    path('pretty/list/', views.pretty_list, name="pretty_list"),
    path('pretty/add/',views.pretty_add,name='pretty_add'),
    path('pretty/<int:nid>/edit/',views.pretty_edit, name="pretty_edit"),
    path('pretty/<int:nid>/delete', views.pretty_delete,name="pretty_delete" )

]
