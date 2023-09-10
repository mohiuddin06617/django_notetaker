from django import forms
from .models import Note
from markdown import markdown


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content_raw']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['content_raw'].widget.attrs.update(
            {'class': 'form-control', 'rows': '4', 'id': "tinymce-mytextarea"}
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.content_html = markdown(instance.content_raw)

        if commit:
            instance.save()

        return instance
