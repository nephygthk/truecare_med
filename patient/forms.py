from django import forms

from account.models import Payment


class PaymentForm(forms.ModelForm):
    payment_summary = forms.CharField(
        label='Receipt Summary', widget=forms.Textarea(attrs={'rows':3, 'cols':15}),)
    
    class Meta:
        model = Payment
        fields = '__all__'
        exclude = ['date_created', 'date_updated', 'patient']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})