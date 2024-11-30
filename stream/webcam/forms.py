from django import forms
from .models import Account
class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['uname', 'name', 'psw', 'email', 'phone']
        # uname = forms.CharField(max_length=100)
        # name = forms.CharField(max_length=100)
        # psw = forms.CharField(widget=forms.PasswordInput)
        # email = forms.EmailField()
        # phone = forms.CharField(max_length=15)