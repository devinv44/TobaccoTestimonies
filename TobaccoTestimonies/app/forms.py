from django import forms

class QuerySettingsForm(forms.Form):
    topic = forms.CharField(max_length = 250)
