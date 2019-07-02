from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class KeyForm(forms.Form):
    primary_key = forms.CharField(label='primary_key', max_length=8, widget=forms.TextInput(attrs={'placeholder': 'key'}))
    primary_remark = forms.CharField(label='primary_remark', max_length=32, required=False, widget=forms.TextInput(attrs={'placeholder': 'remark'}))

    secondary_key = forms.CharField(label='secondary_key', max_length=8, required=False, widget=forms.TextInput(attrs={'placeholder': 'key'}))
    secondary_remark = forms.CharField(label='secondary_remark', max_length=32, required=False, widget=forms.TextInput(attrs={'placeholder': 'remark'}))

    ternary_key = forms.CharField(label='ternary_key', max_length=8, required=False, widget=forms.TextInput(attrs={'placeholder': 'key'}))
    ternary_remark = forms.CharField(label='ternary_remark', max_length=32, required=False, widget=forms.TextInput(attrs={'placeholder': 'remark'}))

    quartus_key = forms.CharField(label='quartus_key', max_length=8, required=False, widget=forms.TextInput(attrs={'placeholder': 'key'}))
    quartus_remark = forms.CharField(label='quartus_remark', max_length=32, required=False, widget=forms.TextInput(attrs={'placeholder': 'remark'}))

    fifth_key = forms.CharField(label='fifth_key', max_length=8, required=False, widget=forms.TextInput(attrs={'placeholder': 'key'}))
    fifth_remark = forms.CharField(label='fifth_remark', max_length=32, required=False, widget=forms.TextInput(attrs={'placeholder': 'remark'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('primary_key', css_class='form-group col-md-2 mb-0'),
                Column('primary_remark', css_class='form-group col-md-10 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('secondary_key', css_class='form-group col-md-2 mb-0'),
                Column('secondary_remark', css_class='form-group col-md-10 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ternary_key', css_class='form-group col-md-2 mb-0'),
                Column('ternary_remark', css_class='form-group col-md-10 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('quartus_key', css_class='form-group col-md-2 mb-0'),
                Column('quartus_remark', css_class='form-group col-md-10 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fifth_key', css_class='form-group col-md-2 mb-0'),
                Column('fifth_remark', css_class='form-group col-md-10 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'submit')
        )