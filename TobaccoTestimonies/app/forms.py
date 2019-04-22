from django import forms

class QuerySettingsForm(forms.Form):
    GLOVE_CHOICES = (
        ('1', 'Common Crawl'),
        ('2', 'Wikipedia 2014 + Gigaword 5'),
        ('3', 'Twitter')
    )

    glove = forms.ChoiceField(choices=GLOVE_CHOICES)
    topic = forms.CharField(max_length = 250)
    person = forms.CharField(max_length = 250)
