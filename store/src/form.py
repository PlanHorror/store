from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div
from crispy_forms.bootstrap import FieldWithButtons, StrictButton
class Profile_Form(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Div(
            Div('parent_name',),
        ),
    )
    class Meta:
        model = Profile
        fields = ['parent_name']
        labels = {'parent_name': 'Họ và tên phụ huynh'}
class SignUpForm(UserCreationForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Div(
            Div('email'),
            Div('username'),
            Div(FieldWithButtons('password1', StrictButton('<i class="fa fa-eye"></i>', type='button', css_class='btn btn-outline-secondary', id='password1Button')),
                ),
            Div(FieldWithButtons('password2', StrictButton('<i class="fa fa-eye"></i>', type='button', css_class='btn btn-outline-secondary', id='password2Button')),
                ),
        ),
    )
    class Meta:
        model = User
        fields = [ 'email', 'username', 'password1', 'password2']
        labels = {'email': 'Email (nếu có)', 'password1': 'Mật khẩu', 'password2': 'Xác nhận mật khẩu', 'username':'Họ và tên bé (hoặc biệt danh)'} # labels for the fields
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
class SignInForm(forms.Form):
    username = forms.CharField(label='Tên đăng nhập')
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)
         
        