from django.test import TestCase

from pedais.forms import ERRO_ITEM_DUPLICADO, ERRO_ITEM_VAZIO, \
    PedalExistenteNoGrupoForm, PedalForm
from pedais.models import Grupo, Pedal


class HomePageTeste(TestCase):

    def test_usa_template_home(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_usa_form_pedal(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], PedalForm)

class GrupoViewTeste(TestCase):

    def test_usa_template_de_grupo(self):
        grupo = Grupo.objects.create()
        response = self.client.get(f'/grupos/{grupo.id}/')

        self.assertTemplateUsed(response, 'grupo.html')

    def test_mostra_apenas_pedais_de_um_grupo(self):
        grupo_correto = Grupo.objects.create()
        Pedal.objects.create(destino='Passaúna', grupo=grupo_correto)
        Pedal.objects.create(destino='Quiriri', grupo=grupo_correto)

        outro_grupo = Grupo.objects.create()
        Pedal.objects.create(destino='Outro Pedal 1', grupo=outro_grupo)
        Pedal.objects.create(destino='Outro Pedal 2', grupo=outro_grupo)

        response = self.client.get(f'/grupos/{grupo_correto.id}/')

        self.assertContains(response, 'Passaúna')
        self.assertContains(response, 'Quiriri')
        self.assertNotContains(response, 'Outro Pedal 1')
        self.assertNotContains(response, 'Outro Pedal 2')

    def test_passa_o_grupo_correto_para_o_template(self):
        outro_grupo = Grupo.objects.create()
        grupo_correto = Grupo.objects.create()

        response = self.client.get(f'/grupos/{grupo_correto.id}/')
        self.assertEqual(response.context['grupo'], grupo_correto)

    def test_pode_salvar_uma_requisicao_POST_a_grupo_existente(self):
        outro_grupo = Grupo.objects.create()
        grupo_correto = Grupo.objects.create()

        self.client.post(
            f'/grupos/{grupo_correto.id}/', data={'destino':'Novo pedal para grupo existente'})

        self.assertEqual(Pedal.objects.count(), 1)
        novo_pedal = Pedal.objects.first()
        self.assertEqual(novo_pedal.destino, 'Novo pedal para grupo existente')
        self.assertEqual(novo_pedal.grupo, grupo_correto)

    def test_redireciona_para_a_view_de_do_grupo(self):
        outro_grupo = Grupo.objects.create()
        grupo_correto = Grupo.objects.create()

        response = self.client.post(
            f'/grupos/{grupo_correto.id}/', 
            data={'destino': 'Novo pedal para grupo existente'}
        )

        self.assertRedirects(response, f'/grupos/{grupo_correto.id}/')

    def post_com_input_invalido(self):
        grupo = Grupo.objects.create()
        return self.client.post(
            f'/grupos/{grupo.id}/',
            data={'destino': ''}
        )
    
    def test_input_invalido_nada_saldo_no_db(self):
        self.post_com_input_invalido()
        self.assertEquals(Pedal.objects.count(), 0)
    
    def test_input_invalido_renderiza_template_grupo(self):
        response = self.post_com_input_invalido()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grupo.html')
    
    def test_para_input_invalido_pass_form_para_o_template(self):
        response = self.post_com_input_invalido()
        self.assertIsInstance(response.context['form'], PedalForm)
    
    def test_para_input_invalido_mostra_mensagem_de_erro(self):
        self.assertContains(self.post_com_input_invalido(), ERRO_ITEM_VAZIO)

    def test_validacao_de_item_duplicado_vai_para_a_pagina_de_grupo(self):

        grupo = Grupo.objects.create()
        pedal = Pedal.objects.create(destino='textey', grupo=grupo)

        response = self.client.post(
            f'/grupos/{grupo.id}/',
            data={'destino': 'textey'}
        )

        self.assertContains(response, ERRO_ITEM_DUPLICADO)
        self.assertTemplateUsed(response, 'grupo.html')
        self.assertEqual(Pedal.objects.all().count(), 1 )

    def test_passa_form_para_template_apos_input_invalido(self):
        response = self.post_com_input_invalido()
        self.assertIsInstance(response.context['form'], PedalExistenteNoGrupoForm)

    def test_mostra_form_do_pedal(self):
        grupo = Grupo.objects.create()
        response = self.client.get(f'/grupos/{grupo.id}/')
        self.assertIsInstance(response.context['form'], PedalExistenteNoGrupoForm)
        self.assertContains(response, 'name="destino"')

class NovoGrupoTeste(TestCase):

    def test_pode_salvar_uma_requisicao_POST(self):

        self.client.post('/grupos/novo', data={'destino': 'Um novo pedal'})
        self.assertEqual(Pedal.objects.count(), 1)
        novo_pedal = Pedal.objects.first()
        self.assertEqual(novo_pedal.destino, 'Um novo pedal')

    def test_redireciona_apos_POST(self):
        response = self.client.post('/grupos/novo', data={'destino': 'Um novo pedal'})
        novo_grupo = Grupo.objects.first()
        self.assertRedirects(response, f'/grupos/{novo_grupo.id}/')

    def test_erros_de_validacao_sao_enviados_novamente_ao_home_template(self):
        response = self.client.post('/grupos/novo', data={'destino': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, ERRO_ITEM_VAZIO)

    def test_pedais_invalidos_nao_sao_salvos(self):
        self.client.post('/grupos/novo', data={'destino': ''})
        self.assertEqual(Grupo.objects.count(), 0)
        self.assertEqual(Pedal.objects.count(), 0)

    def test_input_invalido_renderiza_template_home(self):
        response = self.client.post('/grupos/novo', data={'destino':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')