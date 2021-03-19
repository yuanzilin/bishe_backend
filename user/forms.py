from django import forms


class UserForm_test(forms.Form):
    type = forms.CharField(max_length=100)
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', max_length=100)
    email = forms.CharField(label='邮箱', max_length=100)