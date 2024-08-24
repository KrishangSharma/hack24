from django import forms
from django.contrib.auth.models import User
from .models import Chat, UserProfile
from django.contrib.auth.forms import PasswordChangeForm

class DashboardFilterForm(forms.Form):
    start_date=forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}))
    end_date=forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}))
    sentiment_category=forms.ChoiceField(required=False, choices=[('', 'All'), ('Positive', 'Positive'), ('Negative', 'Negative'), ('Neutral', 'Neutral')])
    user = forms.ModelChoiceField(required=False, queryset=User.objects.all(), empty_label="All Users")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['first_name', 'last_name', 'email', 'sub_county', 'ward']

class UpdateChatStatusForm(forms.ModelForm):
    class Meta:
        model=Chat
        fields=['status']


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove the default password validators
        self.fields['new_password1'].validators = []
        self.fields['new_password2'].validators = []

    # Optionally, you can add your own custom validators if needed
        

class ChatFilterForm(forms.Form):
    user=forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    category=forms.CharField(max_length=10, required=False)
    status=forms.ChoiceField(choices=Chat.STATUS_CHOICES, required=False)