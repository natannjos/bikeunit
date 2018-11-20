from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from pedais.models import Grupo, Pedal

class GrupoEPedalTest(TestCase):

    def test_pedal_esta_relacionado_a_grupo(self):
        grupo = Grupo.objects.create()
        pedal = Pedal()
        pedal.grupo = grupo
        pedal.save()
        self.assertIn(pedal, grupo.pedal_set.all())

    def test_PODE_salvar_pedais_iguais_em_grupos_diferentes(self):
        grupo1 = Grupo.objects.create()
        grupo2 = Grupo.objects.create()

        Pedal.objects.create(destino='Quiriri', grupo=grupo1)
        pedal = Pedal.objects.create(destino='Quiriri', grupo=grupo2)
        pedal.full_clean() # não deve lançar o erro

    def test_ordenacao_de_grupo(self):
    
        grupo = Grupo.objects.create()

        pedal1 = Pedal.objects.create(destino='pedal1', grupo=grupo)
        pedal2 = Pedal.objects.create(destino='pedal2', grupo=grupo)
        pedal3 = Pedal.objects.create(destino='pedal3', grupo=grupo)

        self.assertEquals(
            list(Pedal.objects.all()),
            [pedal1, pedal2, pedal3]
        )

    def test_pedais_duplicados_sao_invalidos(self):
        grupo = Grupo.objects.create()
        Pedal.objects.create(destino='Quiriri', grupo=grupo)

        with self.assertRaises(IntegrityError):
            pedal = Pedal.objects.create(destino='Quiriri', grupo=grupo)
            pedal.full_clean()
            #pedal.save()


class GrupoModelTeste(TestCase):

    def test_get_absolute_url(self):
        grupo = Grupo.objects.create()
        self.assertEqual(grupo.get_absolute_url(), f'/grupos/{grupo.id}/')


class PedalModelTest(TestCase):
    
    def test_texto_padrao(self):
        pedal = Pedal()
        self.assertEqual(pedal.destino, '')

    def test_nao_salva_pedal_vazio(self):
        grupo = Grupo.objects.create()
        pedal = Pedal(grupo=grupo, destino='')

        with self.assertRaises(ValidationError):
            pedal.save()
            pedal.full_clean()

    def test_representacao_por_string(self):
        pedal = Pedal(destino='pedal')
        self.assertEquals(str(pedal), 'pedal')