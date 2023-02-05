from django import forms
from emoji_picker.widgets import EmojiPickerTextareaAdmin
from friends.models import FriendChat


class FriendChatForm(forms.ModelForm):
    text = forms.CharField(widget=EmojiPickerTextareaAdmin, required=False)

    class Meta:
        model = FriendChat
        fields = ('text', 'file')