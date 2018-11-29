from django.conf.urls import url
import contas.views as contas_views


urlpatterns = [
    url(r'^envia_email_login$',
        contas_views.envia_email_login,
        name='envia_email_login'),
    url(r'^login',
        contas_views.login, name='login')
]
