from django import forms
from .models import Concert,QticketsSalesInfo, TargetInfo
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['id', 'name', 'city', 'concert_date','spreadSheetPositon']
        widgets = {
            'spreadSheetPositon': forms.HiddenInput()
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control mb-3 mt-2'
        self.fields['city'].widget.attrs['class'] = 'form-select mb-3 mt-2'
        self.fields['concert_date'].widget.attrs['class'] = 'form-control mb-3 mt-2'

class SaleForm(forms.ModelForm):
    class Meta:
        model = QticketsSalesInfo
        fields = ['qticketsConcertID','qticketsAccountName','spreadSheetQticketsPosition']
        widgets = {
            'spreadSheetQticketsPosition': forms.HiddenInput()
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['qticketsConcertID'].widget.attrs['class'] = 'form-control mb-3 '
        self.fields['qticketsAccountName'].widget.attrs['class'] = 'form-select mb-3 '

class SaleCreateForm(forms.ModelForm):
    class Meta:
        model = QticketsSalesInfo
        fields = ['qticketsConcertID', 'cat', 'qticketsAccountName','spreadSheetQticketsPosition']
        widgets = {
            'spreadSheetQticketsPosition': forms.HiddenInput()
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['cat'].widget.attrs['class'] = 'form-select mb-3 '
        self.fields['qticketsConcertID'].widget.attrs['class'] = 'form-control mb-3 '
        self.fields['qticketsAccountName'].widget.attrs['class'] = 'form-select mb-3 '

class TargetForm(forms.ModelForm):
    class Meta:
        model = TargetInfo
        fields = ['targetAccountID','targetCompanyID']
        widgets = {
            'spreadSheetTargetPosition': forms.HiddenInput()
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['targetAccountID'].widget.attrs['class'] = 'form-control mb-3 '
        self.fields['targetCompanyID'].widget.attrs['class'] = 'form-control mb-3 '

class TargetCreateForm(forms.ModelForm):
    class Meta:
        model = TargetInfo
        fields = '__all__'
        widgets = {
            'spreadSheetTargetPosition': forms.HiddenInput()
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['cat'].widget.attrs['class'] = 'form-select mb-3 '
        self.fields['targetAccountID'].widget.attrs['class'] = 'form-control mb-3 '
        self.fields['targetCompanyID'].widget.attrs['class'] = 'form-control mb-3 '

class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user