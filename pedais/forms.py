from django.core.exceptions import ValidationError
from .models import Pedal
from django import forms

ERRO_ITEM_VAZIO = 'Este campo não pode estar vazio.'
ERRO_ITEM_DUPLICADO = 'Você já adicionou este pedal na lista.'

class PedalForm(forms.models.ModelForm):
    class Meta:
        model = Pedal
        fields = ('destino', )
        widgets = {
            'destino': forms.fields.TextInput(attrs={
                'class': 'form-control input-lg',
                'placeholder': 'Informe o destino do pedal',
            }),
        }
        error_messages = {
            'destino': {'required' : ERRO_ITEM_VAZIO}
        }

    def save(self, grupo):
        self.instance.grupo = grupo
        return super().save()

class PedalExistenteNoGrupoForm(PedalForm):

    def __init__(self, grupo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.grupo = grupo

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e :
            e.error_dict = {'destino':[ERRO_ITEM_DUPLICADO]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)