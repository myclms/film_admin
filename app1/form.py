from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from app1 import models
from app1.utils.bootstrap import BootstrapModelForm, BootstrapForm
from app1.utils.encrypt import md5



class RegisterForm(BootstrapModelForm):
    confirm = forms.CharField(max_length=32, label="确认密码",widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = models.User
        fields = ["name", "password", "confirm", "age", "gender",]

        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }
    
    def clean_password(self):
        password = md5(self.cleaned_data.get("password"))
        return password
    
    def clean_confirm(self):
        confirm = md5(self.cleaned_data.get("confirm"))
        if confirm != self.cleaned_data.get("password"):
            raise ValidationError("两次输入密码不一致")
        return confirm

    
class LoginForm(BootstrapForm):
    name = forms.CharField(
        label = "用户名",
        widget = forms.TextInput,
    )
    password = forms.CharField(
        label = "密码",
        widget = forms.PasswordInput(render_value=True),
    )

    def clean_password(self):
        password = md5(self.cleaned_data.get("password"))
        return password


class UserpasswordeditForm(BootstrapModelForm):
    password = forms.CharField(max_length=64, label="原密码",widget=forms.PasswordInput(render_value=True))
    confirm = forms.CharField(max_length=64, label="确认密码",widget=forms.PasswordInput(render_value=True))
    new = forms.CharField(max_length=64, label="新密码",widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = models.User
        fields = ["password", "new", "confirm"]

    def clean_password(self):
        password = md5(self.cleaned_data.get("password"))
        if password != self.instance.password:
            raise ValidationError("密码输入错误")
        return password
    
    def clean_new(self):
        new_password = md5(self.cleaned_data.get("new"))
        return new_password

    def clean_confirm(self):
        confirm = md5(self.cleaned_data.get("confirm"))
        new_password = self.cleaned_data.get("new")
        if confirm != new_password:
            raise ValidationError("两次密码输入不一致")
        return confirm 


class UserinfoeditForm(BootstrapModelForm):
    confirm = forms.CharField(max_length=64, label="输入用户密码",widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = models.User
        fields = ["name", "password", "confirm", "age", "gender",]

        widgets = {
            "password": forms.PasswordInput(render_value=True, attrs={"readonly":"readonly"}),
        }
    
    # def clean_password(self):
    #     password = self.cleaned_data.get("password")
    #     if password == self.instance.password:
    #         return password
        
    #     return md5(password)
    
    def clean_confirm(self):
        confirm = md5(self.cleaned_data.get("confirm"))
        password = self.cleaned_data.get("password")
        if confirm != password:
            raise ValidationError("密码验证失败")
        return confirm 
    
class FilmForm(BootstrapModelForm):
    def __init__(self, dir_choices=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if dir_choices:
            lovedir = forms.ModelMultipleChoiceField(queryset=dir_choices, widget=forms.SelectMultiple(attrs={"class":"form-control"}),
                                                 label = "选择收藏夹", validators=[])
            self.fields["lovedir"] = lovedir
            
    class Meta:
        model = models.Film
        fields = ["name", "year", "types", "nationality", "cover", "score", "comment", "directors", "actors"]

    def clean_types(self):
        data = self.cleaned_data.get("types", "")
        if type(data) != type(""):
            if data == None:
                data = "暂无"
            else:
                data = str(data)
        if '/' in data or data == "" or data == "暂无":
            pass
        else:
            raise ValidationError("影片类型输入格式保证为 : 类型 / 类型 / ...,只有一个类型也请在最后加'/'")
        return data
    
    def clean_directors(self):
        data = self.cleaned_data.get("directors", "")
        if type(data) != type(""):
            if data == None:
                data = "暂无"
            else:
                data = str(data)
        if '/' in data or data == "" or data == "暂无":
            pass
        else:
            raise ValidationError("导演列表输入格式保证为 : 类型 / 类型 / ...,只有一位导演也请在最后加'/'")
        return data
    
    def clean_actors(self):
        data = self.cleaned_data.get("actors", "")
        if type(data) != type(""):
            if data == None:
                data = "暂无"
            else:
                data = str(data)
        if '/' in data or data == "" or data == "暂无":
            pass
        else:
            raise ValidationError("主演列表输入格式保证为 : 类型 / 类型 / ...,只有一位主演也请在最后加'/'")
        return data
