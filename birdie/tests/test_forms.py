import pytest
from .. import forms
pytestmark = pytest.mark.django_db

class TestPostCreateView:
    def test_form(self):
        form = forms.PostForm(data={})
        assert form.is_valid() == False, 'Should be invalid if, no data is present in the form.'

        form = forms.PostForm(data={'body':'Hello'})
        assert form.is_valid() == False, 'Should be invalid if, message is to short (min of 10).'
        assert 'body' in form.errors, 'Should jabe body field error'

        form = forms.PostForm(data={'body':'Hello World!!!!!!!!!!'})
        assert form.is_valid() == True, 'Form is valid.'
