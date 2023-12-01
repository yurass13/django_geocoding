"""Geocoding forms"""
from django import forms


class SearchForm(forms.Form):
    """Default search Address Form"""
    query = forms.CharField()
