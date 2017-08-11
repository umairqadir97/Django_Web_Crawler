from django import forms


class InputForm(forms.Form):
    home_url = forms.CharField(label='Enter Homepage URL Here:  ', max_length=100)
    number_of_threads = forms.IntegerField(label="Enter Number of Threads:  ", max_value=20 )
    google_code = forms.BooleanField(label=" Google Analytics Code:  ", required=False)
    broken_links = forms.BooleanField(label=" Check Broken Links:  ", required=False)