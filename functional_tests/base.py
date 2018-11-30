import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time

ESPERA_MAXIMA = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def espera(fn):
        def fn_alterada(*args, **kwargs):
            inicio = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - inicio > ESPERA_MAXIMA:
                        raise e
                    time.sleep(0.5)
        return fn_alterada

    def espera_por_linha_em_lista_de_tabela(self, texto_linha):
        inicio = time.time()

        while True:
            try:
                tabela = self.browser.find_element_by_id('id_tabela_pedais')
                linhas = tabela.find_elements_by_tag_name('tr')
                self.assertIn(texto_linha, [linha.text for linha in linhas])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - inicio > ESPERA_MAXIMA:
                    raise e
                time.sleep(2)
    
    @espera
    def espera_por(self, fn):
        return fn()

    def get_destino_input_box(self):
        return self.browser.find_element_by_id('id_destino')

    @espera
    def espera_login(self, email):
        self.browser.find_element_by_link_text('Sair')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @espera
    def espera_logout(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
        