from django import forms
from .models import Comment


class UploadFileForm(forms.Form):
    filename = forms.CharField(max_length=50)
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        labels = {
            'body': 'Comment',
        }
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {
            'body': 'reply',
        }
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }
