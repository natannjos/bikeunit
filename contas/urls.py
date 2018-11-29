from django.conf.urls import url
import contas.views as contas_views
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^envia_email_login$',
        contas_views.envia_email_login,
        name='envia_email_login'),
    url(r'^login',
        contas_views.login, name='login'),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout')
]
