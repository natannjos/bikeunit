from django.test import TestCase
from unittest.mock import patch, call
from contas.models import Token


class EnviaEmailDeLoginViewTest(TestCase):

    def test_redireciona_para_home(self):
        response = self.client.post('/contas/envia_email_login', data={
            'email': 'erlon@email.com'
        })

        self.assertRedirects(response, '/')
    def test_criar_token_associado_com_email(self):
        self.client.post('/contas/envia_email_login', data={
            'email': 'erlon@email.com'
        })

        token = Token.objects.first()
        self.assertEqual(token.email, 'erlon@email.com')

    @patch('contas.views.send_mail')
    def test_envia_email_para_endereco_via_post(self, mock_send_mail):
        self.client.post('/contas/envia_email_login', data={
            'email': 'erlon@email.com'
        })

        self.assertTrue(mock_send_mail.called)

        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args

        self.assertEqual(subject, 'Seu link para login no BikeUnit')
        self.assertEqual(from_email, 'noreply@bikeunit.com')
        self.assertEqual(to_list, ['erlon@email.com'])

    @patch('contas.views.messages')
    def test_adiciona_menssagem_de_sucesso(self, mock_messages):
        response = self.client.post(
            '/contas/envia_email_login', data={
                'email': 'erlon@email.com'
            })

        esperado = 'Verifique seu email, te enviamos um link para que você possa acessar.'
        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, esperado)
        )

    @patch('contas.views.send_mail')
    def test_envia_link_para_login_usando_token_uid(self, mock_send_mail):
        self.client.post('/contas/envia_email_login', data={
            'email': 'erlon@email.com'
        })

        token = Token.objects.first()
        url_esperada = f'http://testserver/contas/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(url_esperada, body)

@patch('contas.views.auth')
class LoginViewTest(TestCase):

    def test_redireciona_para_home(self, mock_auth):
        response = self.client.get('/contas/login?token=abc123')
        self.assertRedirects(response, '/')

    def test_chama_authenticate_com_uid_do_get_request(self, mock_auth):
        self.client.get('/contas/login?token=abcd123')

        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcd123')
        )
    
    def test_chama_auth_login_com_usuario_se_nao_existir_nenhum(self, mock_auth):
        response = self.client.get('/contas/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_nao_loga_se_usuario_nao_esta_autenticado(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/contas/login?token=abcd123')
        self.assertEqual(mock_auth.login.called, False)
