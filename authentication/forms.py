from django.forms import ModelForm
from authentication.models import Student
from authentication.models import Instructor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
import authentication.constants as CONSTANTS



class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'entrance_year', 'major', 'description', ]

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['entrance_year'].required = False
        self.fields['major'].required = False
        self.fields['description'].required = False

class InstructorForm(ModelForm):

    class Meta:
        model = Instructor
        fields = ['first_name', 'last_name', 'rank', 'description', ]

    def __init__(self, *args, **kwargs):
        super(InstructorForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['rank'].required = False
        self.fields['description'].required = False

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password"]



    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

