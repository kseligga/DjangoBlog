from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CommentForm(forms.Form):
    my_name = forms.CharField(max_length=64, validators=[
    ])
    comment = forms.CharField(max_length=128, widget=forms.Textarea)

    def clean(self):
        n = len(self.data["comment"])
        if n < 10:
            raise ValidationError('Come on, write a longer comment, share your thoughts ;)')
        if n > 128:
            raise ValidationError('Log in or register to write longer comments!')

    def clean_my_name(self):
        my_name = self.cleaned_data.get('my_name')
        if User.objects.filter(username=my_name).exists():
            raise ValidationError('This author name is already in use by a registered user')
        return my_name

    def clean_longname(self):
        n = len(self.data["my_name"])
        if n > 64:
            raise ValidationError('Your username is too long')


class CommentLoggedForm(forms.Form):
    comment = forms.CharField(max_length=1000, widget=forms.Textarea)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    reason = forms.ChoiceField(
        choices=[
            ('Posting on forum', 'Posting on forum'),
            ('Browsing blog', 'Browsing blog'),
            ('Just wanted to say hi :)', 'Just wanted to say hi :)'),
            ('I want my epilepsy test results', 'I want my epilepsy test results')
        ],
        widget=forms.Select
    )
    birthDate = forms.DateField(input_formats=['%Y-%m-%d'],
                                widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    sex = forms.ChoiceField(
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female')
        ],
        widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'reason', 'birthDate']


class ResponseForm(forms.Form):
    response = forms.CharField(max_length=1000, widget=forms.Textarea)


class ThreadForm(forms.Form):
    title = forms.CharField(max_length=100, validators=[
    ])
    content = forms.CharField(max_length=1000, widget=forms.Textarea)

    def clean_longtitle(self):
        n = len(self.data["title"])
        if n > 100:
            raise ValidationError('Title of your thread is too long')


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)


class PasswordResetConfirmForm(SetPasswordForm):
    pass
