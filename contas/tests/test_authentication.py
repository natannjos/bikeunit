from django.test import TestCase
from contas.authentication import PasswordlessAuthenticationBackend
from contas.models import Token, User

class AuthenticateTest(TestCase):

    def test_retorna_usuario_nao_encontrado(self):
        resultado = PasswordlessAuthenticationBackend().authenticate('não é um usuário')

        self.assertIsNone(resultado)

    def test_retorna_usuario_existente_com_email_correto_se_token_existir(self):
        email = 'erlon@email.com'
        usuario_existente = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        usuario = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(usuario_existente, usuario)

    def test_retorna_novo_usuario_com_email_correto_se_token_existir(self):
        email = 'erlon@email.com'
        token = Token.objects.create(email=email)
        novo_usuario = PasswordlessAuthenticationBackend().authenticate(token.uid)
        usuario = User.objects.get(email=email)
        self.assertEqual(novo_usuario, usuario)

class GetUserTest(TestCase):

    def test_get_usuario_por_email(self):
        usuario = User.objects.create(email='joao@email.com')
        usuario_esperado = User.objects.create(email='erlon@email.com')
        usuario_encontrado = PasswordlessAuthenticationBackend().get_user('erlon@email.com')

        self.assertEqual(usuario_encontrado, usuario_esperado)

    def test_retorna_None_se_usuario_com_este_email_nao_existir(self):

        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('erlon@email.com')
        )


