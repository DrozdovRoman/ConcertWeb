from django import forms
from .models import Concert,QticketsSalesInfo, TargetInfo

class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control mb-3 '
        self.fields['city'].widget.attrs['class'] = 'form-select mb-3 '
        self.fields['concert_date'].widget.attrs['class'] = 'form-control mb-3'
        self.fields['status'].widget.attrs['class'] = 'form-select mb-3'

class SaleForm(forms.ModelForm):
    class Meta:
        model = QticketsSalesInfo
        fields = ['qticketsConcertID','qticketsAccountName']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['qticketsConcertID'].widget.attrs['class'] = 'form-control mb-3 '
        self.fields['qticketsAccountName'].widget.attrs['class'] = 'form-control mb-3 '

class SaleCreateForm(forms.ModelForm):
    class Meta:
        model = QticketsSalesInfo
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['cat'].widget.attrs['class'] = 'form-select mb-3 '
        self.fields['qticketsConcertID'].widget.attrs['class'] = 'form-control mb-3 '
        self.fields['qticketsAccountName'].widget.attrs['class'] = 'form-control mb-3 '

class TargetForm(forms.ModelForm):
    class Meta:
        model = TargetInfo
        fields = ['targetAccountID','targetCompanyID']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['targetAccountID'].widget.attrs['class'] = 'form-control mb-3 '
        self.fields['targetCompanyID'].widget.attrs['class'] = 'form-control mb-3 '

class TargetCreateForm(forms.ModelForm):
    class Meta:
        model = TargetInfo
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['cat'].widget.attrs['class'] = 'form-select mb-3 '
        self.fields['targetAccountID'].widget.attrs['class'] = 'form-control mb-3 '
        self.fields['targetCompanyID'].widget.attrs['class'] = 'form-control mb-3 '