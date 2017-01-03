from django.conf.urls import url
from rango import views

urlpatterns = [
      url(r'^$', views.index, name = 'index'),
      url(r'^about/$', views.about, name = 'about'),
      url(r'^add_category/$', views.add_category, name='add_category'),
      url(r'^category/(?P<category_enc_name>[\w\-]+)/add_page/$', views.add_page, name = 'add_page'),
      url(r'^category/(?P<category_enc_name>[\w\-]+)/$', views.show_category, name='show_category'),
      url(r'^register/$', views.register, name='register'),
      url(r'^login/$', views.user_login, name='login'),
      url(r'^check/$', views.check_logged_in, name='check'),
      url(r'^restricted/$', views.restricted, name='restricted'),
      url(r'^logout/$', views.user_logout, name='logout'),
]

#IMPORTANT - note that the parameters included in the url are declared in the corresponding view

