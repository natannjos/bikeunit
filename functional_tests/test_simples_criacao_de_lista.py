
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NovoVisitanteTest(FunctionalTest):

    def test_pode_iniciar_um_grupo_para_um_usuario(self):

        # Erlon ouviu falar a respeito de um novo app de viagem de bikes. 
        # Ele foi checar a homepage
        self.browser.get(self.live_server_url)

        # Ele notou que o título da página e o cabeçao mencionam Bikeunit
        self.assertIn('BikeUnit', self.browser.title)
        texto_cabecalho = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('BikeUnit', texto_cabecalho)

        # Ele vê uma caixa de texto para informar o destino do pedal
        caixa_de_texto = self.get_destino_input_box()
        placeholder = caixa_de_texto.get_attribute('placeholder')
        self.assertEqual(
            placeholder,
            'Informe o destino do pedal'
        )

        # Ele digita "Passaúna" em uma caixa de texto (o destino do próximo pedal)
        caixa_de_texto.send_keys('Passaúna')

        # Quando ele clica enter, a página recarrega e agora a página lista 
        # "Pedal para Passaúna" como um item em uma tabela de destinos de pedais
        caixa_de_texto.send_keys(Keys.ENTER)
        self.espera_por_linha_em_lista_de_tabela('1: Passaúna')

        # Ainda há a caixa de texto pedindo para inserir um novo destino. 
        # Ele digita "Quiriri" e da enter
        caixa_de_texto = self.get_destino_input_box()
        caixa_de_texto.send_keys('Quiriri')
        caixa_de_texto.send_keys(Keys.ENTER)

        # A página recarrega novamente, e agora mostra os dois destinos
        self.espera_por_linha_em_lista_de_tabela('1: Passaúna')
        self.espera_por_linha_em_lista_de_tabela('2: Quiriri')

        # Erlon imagina se o site continuará lembrando quais os pedais que ele marcou
        # Então ele percebe que o site tem uma URL única para aquela lista

        # Ele visita a url e a lista ainda está lá

    def test_multiplos_usuarios_podem_comecar_grupos_com_urls_diferentes(self):

        # Erlon cria um novo grupo
        self.browser.get(self.live_server_url)
        caixa_de_entrada = self.get_destino_input_box()
        caixa_de_entrada.send_keys('Passaúna')
        caixa_de_entrada.send_keys(Keys.ENTER)
        self.espera_por_linha_em_lista_de_tabela('1: Passaúna')

        # Ele notou que o grupo agora tem uma url unica
        url_grupo_erlon = self.browser.current_url
        self.assertRegex(url_grupo_erlon, '/grupos/.+')

        # Agora um novo usuario, Sofia, visita o site também

        # Vamos usar uma nova sessão do browser para ter certeza que
        # nenhuma informação de Erlon venha através de cookies e etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Sofia visita a home page. Não há sinal do grupo do Erlon
        self.browser.get(self.live_server_url)
        texto_pagina = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Passaúna', texto_pagina)
        self.assertNotIn('Quiriri', texto_pagina)

        # Sofia começa um novo geupo informando um novo destino de pedal.
        caixa_de_entrada = self.get_destino_input_box()
        caixa_de_entrada.send_keys('Jusita')
        caixa_de_entrada.send_keys(Keys.ENTER)
        self.espera_por_linha_em_lista_de_tabela('1: Jusita')

        # Sofia ganha sua url única
        url_grupo_sofia = self.browser.current_url
        self.assertRegex(url_grupo_sofia, '/grupos/.+')
        self.assertNotEqual(url_grupo_erlon, url_grupo_sofia)

        # Novamente, não há traços da lista de Erlon
        texto_pagina = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Passaúna', texto_pagina)
        self.assertNotIn('Quiriri', texto_pagina)

        # Satisfeitos, eles voltam para suas vidas
