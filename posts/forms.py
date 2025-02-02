from django import forms
from posts.models import PostComments
from emoji_picker.widgets import EmojiPickerTextareaAdmin

# class CreatePostForm(forms.Form):


class PostCommentsForm(forms.ModelForm):
    comment = forms.CharField(widget=EmojiPickerTextareaAdmin)
    required_css_class = "comments_form"

    class Meta:
        model = PostComments
        fields = ('comment',)
