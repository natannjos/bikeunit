from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
User = get_user_model()


class MeusGruposTest(FunctionalTest):

	def cria_sessao_pre_autenticada(self, email):
		user = User.objects.create(email=email)
		session = SessionStore()
		session[SESSION_KEY] = user.pk
		session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
		session.save()

		## para setar um cookie precisamos antes visitar um dominio
		## paginas 404 carregam mais rápido
		self.browser.get(self.live_server_url+'/404_no_such_url/')
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session.session_key,
			path='/'
		))

	def test_listas_de_usuarios_logados_sao_salvas_como_meus_grupos(self):
		email = 'erlon@email.com'
		self.browser.get(self.live_server_url)
		self.espera_logout(email)

		#Erlon é um usuário logado
		self.cria_sessao_pre_autenticada(email)
		self.browser.get(self.live_server_url)
		self.espera_login(email)