from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django import forms
from django.core.validators import RegexValidator


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


# class NumModeForm(forms.ModelForm):
#     class Meta:
#         model = models.PrettyNum
#         fields = ["mobile", "price", "level", "status"]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for name, field in self.fields.items():
#             field.widget.attrs = {"class": "form-control", "placeholder": field.label}

class NumModeForm(forms.ModelForm):
    # ① 用表单字段“覆盖”模型字段：让 mobile 必填 + 正则校验
    mobile = forms.CharField(
        label="号码",
        required=True,
        validators=[RegexValidator(r"^1[3-9]\d{9}$", "手机号格式错误")],
        error_messages={"required": "号码不能为空"},
        help_text="请输入 11 位数字, 数字1开头,第二位不能是1或2",
        widget=forms.TextInput()
    )

    class Meta:
        model = models.PrettyNum
        # fieles = "__all__"
        fields = ["mobile", "price", "level", "status"]
        # exclude = ['level']  除了"level" 以外都循环
        widgets = {
            # ② price 用数字输入框，并加 min 防止负数（前端体验）
            "price": forms.NumberInput(attrs={"min": 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ③ 给每个控件加 bootstrap 样式；注意用 update，不要直接 "=" 覆盖
        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
            })

            # input 才需要 placeholder；select 的 placeholder 基本不生效
            if not isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("placeholder", field.label)

            # 给必填字段一个中文提示
            field.error_messages.setdefault("required", f"{field.label}不能为空")

        # ④ select 做“请选择...”更像真实后台（并且可触发 required）
        self.fields["level"].choices = [("", "请选择等级")] + list(self.fields["level"].choices)
        print(self.fields["level"].choices)
        # [('', '请选择等级'), (1, '一级'), (2, '二级'), (3, '三级'), (4, '四级')]
        self.fields["status"].choices = [("", "请选择状态")] + list(self.fields["status"].choices)

        self.fields["level"].error_messages["required"] = "请选择等级"
        self.fields["status"].error_messages["required"] = "请选择状态"

    def clean_mobile(self):
        """⑤ 拦截重复号码（新增/编辑都能用）"""
        mobile = self.cleaned_data.get("mobile")
        """
        这行代码是 Python（通常见于 Django 框架的表单 / 序列化器处理逻辑）中获取清洗后数据的典型写法，核心作用是安全地从清洗后的数据集里提取 "mobile" 字段的值，逐部分拆解：
        1. self.cleaned_data
        self：代表当前类的实例（比如 Django 表单类 / 序列化器类的实例）；
        cleaned_data：Django 表单 / 序列化器的核心属性，是一个字典（dict），存储经过验证、清洗后的用户输入数据（比如去除空格、格式校验、类型转换后的结果）；
        区别于原始输入（如 request.POST），cleaned_data 是 “干净、可信” 的数据，避免了原始输入的格式错误、非法值等问题。
        2. .get("mobile")
        调用字典的 get() 方法，而非直接 cleaned_data["mobile"]，是为了避免 KeyError 异常：
        如果 "mobile" 字段存在且有值，返回对应值；
        如果 "mobile" 字段不存在（比如用户未填写），返回 None（而非报错），让代码更健壮。
        核心场景
        通常用在 Django 表单的 clean() 方法、序列化器的验证方法中，目的是：
        从验证通过的用户输入里，安全获取手机号（mobile）字段的值，后续可用于数据库存储、业务逻辑处理（如短信发送）等。
        """
        qs = models.PrettyNum.objects.filter(mobile=mobile)
        # 如果是编辑页面（self.instance.pk 有值），要排除自己
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("该号码已存在")
        return mobile

    def clean_price(self):
        """⑥ 价格不能为负数（后端强校验）"""
        price = self.cleaned_data.get("price")
        if price is None:
            return 0
        if price < 0:
            raise forms.ValidationError("价格不能小于 0")
        return price


# def pretty_add(request):
#     if request.method == "GET":
#         form = NumModeForm()
#         print(type(form))
#         print(list(form.fields.keys()))
#         target_field = "mobile"
#         if target_field in form.fields:
#             print(f"{target_field},字段类型：",form.fields[target_field])
#         else:
#             print(f"❌ 表单中没有{target_field}字段！")
#         print("✅ 表单初始值：", form.initial)
#         return render(request, 'pretty_add.html', {"form": form})
#     form = NumModeForm(data=request.POST)
#     if form.is_valid():
#         form.save()
#         return redirect("pretty_list")
#     return render(request, 'pretty_add.html', {"form": form})

def pretty_add(request):
    if request.method == "GET":
        form = NumModeForm()
        return render(request, "pretty_add.html", {"form": form})

    form = NumModeForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("pretty_list")

    # 校验失败：把带错误信息、带用户输入的 form 重新扔回模板
    return render(request, "pretty_add.html", {"form": form})


class NumEditModeForm(forms.ModelForm):
    # ① 用表单字段“覆盖”模型字段：让 mobile 必填 + 正则校验
    mobile = forms.CharField(
        label="号码",
        required=True,
        validators=[RegexValidator(r"^1[3-9]\d{9}$", "手机号格式错误")],
        error_messages={"required": "号码不能为空"},
        help_text="请输入 11 位数字, 数字1开头,第二位不能是1或2",
        widget=forms.TextInput(),
        disabled=True
    )

    class Meta:
        model = models.PrettyNum
        # fieles = "__all__"
        fields = ["mobile", "price", "level", "status"]
        # exclude = ['level']  除了"level" 以外都循环
        widgets = {
            # ② price 用数字输入框，并加 min 防止负数（前端体验）
            "price": forms.NumberInput(attrs={"min": 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ③ 给每个控件加 bootstrap 样式；注意用 update，不要直接 "=" 覆盖
        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
            })

            # input 才需要 placeholder；select 的 placeholder 基本不生效
            if not isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("placeholder", field.label)

            # 给必填字段一个中文提示
            field.error_messages.setdefault("required", f"{field.label}不能为空")

        # ④ select 做“请选择...”更像真实后台（并且可触发 required）
        self.fields["level"].choices = [("", "请选择等级")] + list(self.fields["level"].choices)
        print(self.fields["level"].choices)
        # [('', '请选择等级'), (1, '一级'), (2, '二级'), (3, '三级'), (4, '四级')]
        self.fields["status"].choices = [("", "请选择状态")] + list(self.fields["status"].choices)

        self.fields["level"].error_messages["required"] = "请选择等级"
        self.fields["status"].error_messages["required"] = "请选择状态"

    def clean_mobile(self):
        """⑤ 拦截重复号码（新增/编辑都能用）"""
        mobile = self.cleaned_data.get("mobile")
        qs = models.PrettyNum.objects.filter(mobile=mobile)
        # 如果是编辑页面（self.instance.pk 有值），要排除自己
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("该号码已存在")
        return mobile

    def clean_price(self):
        """⑥ 价格不能为负数（后端强校验）"""
        price = self.cleaned_data.get("price")
        if price is None:
            return 0
        if price < 0:
            raise forms.ValidationError("价格不能小于 0")
        return price


# 编辑界面用了另一单独的类，和添加不一样，不允许修改号码，只能修改价格，等级，状态/用disabled=True 实现的
def pretty_edit(request, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = NumEditModeForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": {form}})
    form = NumEditModeForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("pretty_list")
    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).first().delete()
    return redirect("pretty_list")
