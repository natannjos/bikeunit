from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'erlon@exemplo.com'
ASSUNTO = 'Seu link para login no BikeUnit'


class LoginTest(FunctionalTest):

    def test_recebe_link_de_email_para_login(self):
        # Erlon vai para o site do Bikeunit
        # ele nota um seção de login na barra de navegacao pela primeira vez
        # Está dizendo a ele para colocar o email, ele faz isso
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # Uma mensagem aparece dizendo que o email foi enviado
        self.espera_por(lambda: self.assertIn(
            'Verifique seu email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Ele checa seu email e encontra a mensagem
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, ASSUNTO)

        # O email tem um link
        self.assertIn('Use este link para logar', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Não foi possível encontrar a url no email:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # ele clica
        self.browser.get(url)

        # ele está logado
        self.espera_por(
            lambda: self.browser.find_element_by_link_text('Sair')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

        # agora ele sai
        self.browser.find_element_by_link_text('Sair').click()

        # Ele está deslogado
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(TEST_EMAIL, navbar.text)
