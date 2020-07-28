from django import forms
from .models import Schedule
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from django.http import HttpResponse
from unittest.util import _MAX_LENGTH

class ScheduleForm(forms.ModelForm):
    """
    Bootstrap対応フォーム
    """

    class Meta:
        model = Schedule
        fields = ('summary', 'description', 'start_time', 'end_time')
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if end_time <= start_time:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後に設定してください。'
            )
        return end_time

class ContactForm(forms.Form):

    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お名前",
        }),
    )

    email = forms.EmailField(
        label='',
                widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレス",
        }),
    )

    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "お問い合わせ内容",
        }),
    )

    def send_email(self):
        subject = "お問い合わせ"
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        from_email = '{name} <{email}>'.format(name=name, email=email)
        message = "送信者：" + email + "\n\n" + self.cleaned_data['message']
        recipient_list = [settings.EMAIL_HOST_USER]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("メール送信時にエラーが発生しました。")
