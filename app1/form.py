from django import forms
from django.core.exceptions import ValidationError

from app1 import models
from app1.utils.bootstrap import BootstrapModelForm, BootstrapForm
from app1.utils.encrypt import md5



class RegisterForm(BootstrapModelForm):
    confirm = forms.CharField(max_length=32, label="确认密码",widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = models.User
        fields = ["name", "password", "confirm", "age", "gender",]

        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if not age:
            return age
        if age <= 0:
           raise ValidationError("年龄不能小于0")

        return age
    
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


class UserinfoeditForm(BootstrapModelForm):
    confirm = forms.CharField(max_length=32, label="确认密码/密码验证",widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = models.User
        fields = ["name", "password", "confirm", "age", "gender",]

        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if not age:
            return age
        if age <= 0:
           raise ValidationError("年龄不能小于0")

        return age
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password == self.instance.password:
            return password
        
        return md5(password)
    
    def clean_confirm(self):
        confirm = md5(self.cleaned_data.get("confirm"))
        password = self.cleaned_data.get("password")
        if confirm != password:
            if password == self.instance.password:
                raise ValidationError("密码错误")
            raise ValidationError("两次输入密码不一致")
        return confirm 