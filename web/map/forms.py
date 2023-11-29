from django import forms


class SearchAddress(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Enter address'}))
    radius = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Radius in km'}))
