from django import forms
from .models import CustomUser,ProductDb

class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password'
        })
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'email', 
            'password', 
            'user_image'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'

        self.fields['username'].label = "Username"
        self.fields['username'].help_text = ""
        self.fields['email'].label = "Email Address"
        self.fields['password'].label = "Password"
        self.fields['user_image'].label = "Profile Image"
        


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input'
            })


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
        widgets = {
            'product_image': forms.FileInput()
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input'
            })