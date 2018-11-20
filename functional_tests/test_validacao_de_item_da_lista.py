from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ValidacaoDeItemTest(FunctionalTest):

    def get_elemento_erro(self):
        return self.browser.find_element_by_css_selector('.has-error')
    
    def test_nao_pode_adicionar_itens_vazios(self):

        # Erlon acidentalmente clica enter e submete um item vazio na home page
        self.browser.get(self.live_server_url)
        self.get_destino_input_box().send_keys(Keys.ENTER)

        # O navegador intercepta a requisição, e não carrega a página do grupo
        self.espera_por(
            lambda: self.browser.find_element_by_css_selector('#id_destino:invalid')
        )

        # Ele começa a digitar algum texto para o novo destino e o erro desaparece
        self.get_destino_input_box().send_keys('Passaúna')
        self.espera_por(
            lambda: self.browser.find_element_by_css_selector('#id_destino:valid')
        )
        

        # Só para testar, ele tenta adicionar novamente um item vazio na página da lista de pedais
        self.get_destino_input_box().send_keys(Keys.ENTER)
        self.espera_por_linha_em_lista_de_tabela('1: Passaúna')

        # Ele tenta submeter um novo destino vazio
        self.get_destino_input_box().send_keys(Keys.ENTER)

        # Novamente o browser reclama
        self.espera_por_linha_em_lista_de_tabela('1: Passaúna')
        self.espera_por(
            lambda: self.browser.find_element_by_css_selector('#id_destino:invalid')
        )

        # E ele conserta escrevendo outro destino
        self.get_destino_input_box().send_keys('Quiriri')
        self.espera_por(
            lambda: self.browser.find_element_by_css_selector('#id_destino:valid')
        )
        self.get_destino_input_box().send_keys(Keys.ENTER)
        self.espera_por_linha_em_lista_de_tabela('1: Passaúna')
        self.espera_por_linha_em_lista_de_tabela('2: Quiriri')

    def test_nao_pode_add_pedais_duplicados(self):

        # Erlon adiciona um pedal em um novo grupo
        self.browser.get(self.live_server_url)
        self.get_destino_input_box().send_keys('Quatro Barras')
        self.get_destino_input_box().send_keys(Keys.ENTER)
        self.espera_por_linha_em_lista_de_tabela('1: Quatro Barras')

        # Acidentalmente ele adiciona o mesmo destino novamente
        self.get_destino_input_box().send_keys('Quatro Barras')
        self.get_destino_input_box().send_keys(Keys.ENTER)

        # Ele recebe uma útil mensagem de erro
        self.espera_por(lambda: self.assertEqual(
            self.get_elemento_erro().text,
            'Você já adicionou este pedal na lista.'
        ))

    def test_mensagens_de_erro_sao_removidas_no_input(self):

        # Erlon adiciona um pedal e causa um erro de validacao
        self.browser.get(self.live_server_url)
        self.get_destino_input_box().send_keys('Repetido')
        self.get_destino_input_box().send_keys(Keys.ENTER)
        self.espera_por_linha_em_lista_de_tabela('1: Repetido')
        self.get_destino_input_box().send_keys('Repetido')
        self.get_destino_input_box().send_keys(Keys.ENTER)

        self.espera_por(lambda: self.assertTrue(
            self.get_elemento_erro().is_displayed()
        ))

        # Ele começa a digitar no input para limparo erro
        self.get_destino_input_box().send_keys('a')

        # Ele fica feliz em perceber que a mensagem sumiu
        self.espera_por(lambda: self.assertFalse(
            self.get_elemento_erro().is_displayed()
        ))
