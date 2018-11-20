from builtins import object

from django.test import TestCase

from pedais.forms import ERRO_ITEM_DUPLICADO, ERRO_ITEM_VAZIO, \
    PedalExistenteNoGrupoForm, PedalForm
from pedais.models import Grupo, Pedal


class PedalFormTest(TestCase):

    def test_form_renderiza_input_pedal(self):
        form = PedalForm()
        self.assertIn('placeholder="Informe o destino do pedal"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
    
    def test_validacao_do_form_para_input_vazio(self):
        form = PedalForm(data={'destino':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['destino'],
            [ERRO_ITEM_VAZIO]
        )

    def test_form_salva_um_grupo_com_seu_proprio_save(self):
        grupo = Grupo.objects.create()
        form = PedalForm(data={'destino': 'destino'})
        novo_pedal = form.save(grupo=grupo)
        self.assertEqual(novo_pedal, Pedal.objects.first())
        self.assertEqual(novo_pedal.destino, 'destino')
        self.assertEqual(novo_pedal.grupo, grupo)


    def test_salva_form(self):
        grupo = Grupo.objects.create()
        form = PedalExistenteNoGrupoForm(grupo=grupo, data={'destino':'oi'})
        novo_pedal = form.save()
        self.assertEqual(Pedal.objects.all()[0], novo_pedal)

class PedalExistenteNaListaTest(TestCase):
    
    def test_form_renderiza_input_pedal(self):
        grupo = Grupo.objects.create()
        form = PedalExistenteNoGrupoForm(grupo=grupo)
        self.assertIn('placeholder="Informe o destino do pedal"', form.as_p())

    def test_validacao_form_input_vazio(self):
        grupo = Grupo.objects.create()
        form = PedalExistenteNoGrupoForm(grupo=grupo, data={'destino':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['destino'], [ERRO_ITEM_VAZIO])

    def test_validacao_de_form_para_itens_duplicados(self):
        grupo = Grupo.objects.create()
        Pedal.objects.create(destino='sem duplicatas', grupo=grupo)
        form = PedalExistenteNoGrupoForm(grupo=grupo, data={'destino':'sem duplicatas'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['destino'], [ERRO_ITEM_DUPLICADO])
