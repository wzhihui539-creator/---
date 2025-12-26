from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django import forms


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


# nid获取id数值，在urls中定义的，如 path('depart/<int:nid>/delete/', views.depart_delete, name="depart_delete"),
# 可以看看urls里的备注
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


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=2, label="用户名")
    password = forms.CharField(min_length=3, label="密码")

    class Meta:
        # 1. 绑定模型
        # 意思就是：这个表单是专门为 models.UserInfo 这个数据库表服务的。
        model = models.UserInfo
        # 2. 选择字段
        # 意思就是：虽然 UserInfo 表里可能有很多列，但我这个表单只显示列表里的这几项。
        # Django 会自动根据模型里的定义（如 IntegerField, CharField）生成对应的前端输入框。
        fields = ["name", 'password', "age", "account", "create_time", "gender", "depart"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 3. 给每个字段的“插件(widget)”添加 HTML 属性(attrs)
            # 这里的 "class": "form-control" 是 Bootstrap 框架的核心样式类。
            # 如果不加这行，生成的输入框就是光秃秃的原生样子，很丑。
            # 加了这行，输入框就会变成 Bootstrap 风格（圆角、高亮、占满宽度）。

            # "placeholder": field.label
            # 意思是把字段的中文名（如“用户名”）自动放到输入框的提示语里（灰色占位符）。
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm
        return render(request, 'user_model_form_add.html', {"form": form})
    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("user_list")
    # 校验失败，在页面上显示错误信息
    return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # === 就是在这里使用！ ===

        # 1. 假设你想强制把账户余额归零，不管用户填了多少
        # form.instance.account = 0

        # 2. 假设有一个字段叫 'editor' (最后编辑者)，表单里没写，你想后台自动加上
        # form.instance.editor = request.user.username

        # === 修改完 form.instance 之后，再保存 ===
        # form.save()
        form.save()
        return redirect("user_list")
    # === 修改这里 ===
    # 错误写法（原代码）：return render(request, "user_list.html", {"form": form})
    # 正确写法：如果校验失败，应该重新渲染编辑页面，并带上包含错误信息的 form
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).first().delete()
    return redirect("user_list")


def pretty_list(request):
    # order_by 按照等级排序“-”代表从高到底
    queryset = models.PrettyNum.objects.all().order_by("-level")
    print(queryset.filter().first().level)
    return render(request, "pretty_list.html", {"queryset": queryset})


class NumModeForm(forms.ModelForm):
    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def pretty_add(request):
    if request.method == "GET":
        form = NumModeForm()
        print(type(form))
        print(list(form.fields.keys()))
        target_field = "mobile"
        if target_field in form.fields:
            print(f"{target_field},字段类型：",form.fields[target_field])
        else:
            print(f"❌ 表单中没有{target_field}字段！")
        print("✅ 表单初始值：", form.initial)
        return render(request, 'pretty_add.html', {"form": {form}})
    form = NumModeForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("pretty_list")
    return render(request, 'pretty_add.html', {"form": form})
