from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class LayoutEEstiloTest(FunctionalTest):

    def test_layout_e_estilos(self):

        # Erlon vai até a home
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Ele nota que a caixa de texto está centralizada
        caixa_de_texto = self.get_destino_input_box()
        caixa_de_texto.send_keys('testando')
        caixa_de_texto.send_keys(Keys.ENTER)
        self.espera_por_linha_em_lista_de_tabela('1: testando')

        caixa_de_texto = self.get_destino_input_box()
        self.assertAlmostEqual(
            caixa_de_texto.location['x'] + caixa_de_texto.size['width'] / 2,
            512, 
            delta=10
        )
