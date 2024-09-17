from django import forms
from .models import MusicCategory, Song

class MusicCategoryForm(forms.ModelForm):
    class Meta:
        model = MusicCategory
        fields = ['name']
        

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'category', 'audio_file']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        audio_file = cleaned_data.get('audio_file')

        if not audio_file:
            raise forms.ValidationError("Please upload an audio file.")