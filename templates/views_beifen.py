from django.shortcuts import render, redirect,HttpResponse
from app01 import models


# Create your views here.

def depart_list(request):
    queryset = models.Department.objects.all()
    return render(request, "depart_list.html", {"queryset": queryset})


# {"queryset": queryset}：传递给模板的上下文数据（字典格式）：
# 键queryset：模板中可通过这个名称访问数据（如模板中写{{ queryset }}或{% for item in queryset %}）；
# 值queryset：视图中定义的变量（通常是查询集，比如从数据库查询的部门列表数据）。


def depart_add(request):
    """添加部门"""
    if request.method == 'GET':
        return render(request, "depart_add.html")

    title = request.POST.get('title')
    models.Department.objects.create(title=title)
    return redirect("depart_list")


def depart_delete(request, nid):
    models.Department.objects.filter(id=nid).delete()
    return redirect("depart_list")


def depart_edit(request, nid):
    # gpt给加了个保护，如果地址栏手动输入nid=999之类的不存在的id会返回到列表界面
    row_object = models.Department.objects.filter(id=nid).first()
    if not row_object:
        return redirect("depart_list")  # 或返回 404

    if request.method == "GET":
        return render(request, "depart_edit.html", {"row_object": row_object})

    title = (request.POST.get("title") or "").strip()
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("depart_list")


def user_list(request):
    queryset = models.UserInfo.objects.all()
    return render(request, "user_list.html", {"queryset": queryset})


def user_add(request):
    if request.method == "GET":
        context = {
            "gender_choices": models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all()
        }
        return render(request, "user_add.html", context)

    name = (request.POST.get("name") or "").strip()
    password = (request.POST.get("password") or "").strip()
    age = request.POST.get("age")
    account = request.POST.get("account")
    ctime = request.POST.get("ctime")
    gender = request.POST.get("gender")
    depart_id = request.POST.get("depart_id")

    if not depart_id:
        return HttpResponse("未选择部门：请检查<select name='depart_id'>是否在<form>内部")

    models.UserInfo.objects.create(
        name=name,
        password=password,
        age=age,
        account=account,
        create_time=ctime,
        gender=gender,
        depart_id=depart_id
    )
    return redirect("user_list")