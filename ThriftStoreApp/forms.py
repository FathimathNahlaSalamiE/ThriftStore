from django import forms
from .models import CustomUser,ProductDb

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password',
            'user_image'
        ]

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AddProductForm(forms.ModelForm):
    class Meta:
        model = ProductDb
        fields = [
            'product_name',
            'product_description',
            'product_category',
            'product_price',
            'product_image'
        ]