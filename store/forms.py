from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='first_name', max_length=30)
    last_name = forms.CharField(label='last_name', max_length=30)
    email = forms.EmailField(label='email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    dob = forms.DateField(label='dob')
    address = forms.CharField(label='address')
    city = forms.CharField()
    state = forms.CharField()
    zip_code = forms.IntegerField(label='zip_code')
    mob_ph = forms.IntegerField(label='mob_ph')