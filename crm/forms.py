from django import forms
from crm import models
from django.core.exceptions import ValidationError

class BaseForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})

#注册
class RegForm(BaseForm):
    password = forms.CharField(
        label='密码',
        widget=forms.widgets.PasswordInput(),
        min_length=4,
        error_messages={'min_length':'最小长度为4'}
    )
    re_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput()
    )
    class Meta:
        model = models.UserProfile
        # 指定字段
        fields = ['username','password','re_password','name','department']
        widgets = {
            'username': forms.widgets.EmailInput(attrs={'class':'form-control'})
        }
        labels = {
            'username':'用户名',
            'password':'密码',
            'name':'姓名',
            'department':'部门',
        }

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd == re_pwd:
            return self.cleaned_data
        self.add_error('re_password','两次密码不一致')
        raise ValidationError('两次密码不一致')