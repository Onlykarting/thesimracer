from django import forms
from playlists.models import Playlist


class PlaylistCreationForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = '__all__'
        required = ('name', )

    def __init__(self, *args, **kwargs):
        super(PlaylistCreationForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['thumbnail'].required = False
