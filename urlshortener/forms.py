from django import forms

from models import ShortURL, key_to_id, id_to_key

class ShortURLForm(forms.ModelForm):

    key = forms.CharField(required=False)

    class Meta:
        model = ShortURL
        fields = ('url', 'key')

    def __init__(self, *args, **kwargs):
        super(ShortURLForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs and kwargs['instance'].id:
            self.initial['key'] = id_to_key(kwargs['instance'].id)

    def clean_key(self):
        try:
            ShortURL.objects.get_by_key(self.cleaned_data['key'])
        except ShortURL.DoesNotExist:
            return self.cleaned_data['key']
        else:
            raise forms.ValidationError('Key is already taken')

    def save(self, commit=True):
        model = super(ShortURLForm, self).save(commit=False)

        if self.cleaned_data.get('key'):
            model.key = self.cleaned_data['key']
        if commit:
            model.save(force_insert=True)

        return model
