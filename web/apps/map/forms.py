"""Map forms"""
from django import forms


class SearchAddress(forms.Form):
    """Default address search from.
    Fields:
        :param address: str - address search string.
        :param radius: int - radius for search other locations.
    """
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Enter address'}))
    radius = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Radius in km'}))
