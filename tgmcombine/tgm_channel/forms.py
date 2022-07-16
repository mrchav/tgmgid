from django import forms

from .models import TgmChannel

class ChannelForm(forms.ModelForm):

    class Meta:
        model = TgmChannel
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 5, 'style': 'form_desc_css'}),
        }
        fields = ('tgmlink','description', )

