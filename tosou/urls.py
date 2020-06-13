from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('logout/',views.logout_view,name='logout'),
    path('index/',views.index_view,name='index'),
    path('check/',views.check_view,name='check'),
    path('simulation/',views.easy_view,name='easy'),
    path('a_simulation/',views.a_easy_view,name='a_easy'),
    path('consul/',views.consul_form_view,name='consul'),
    path('email/',views.email_view,name='email'),
    path('complete/',views.complete_view,name='complete'),
    path('good/',views.good_view,name='good'),
    path('present/',views.present_view,name='present'),
    path('mitumori/',views.mitumori_view,name='mitumori'),
    path('m_form/',views.m_form_view,name='m_form'),
    path('regi/',views.regi_view,name='regi'),
    path('login/',views.login_view,name='login'),
    path('account/',views.account_view,name='account'),
    path('easy_simulation',views.e_s_view,name='e_s'),
    path('page/',views.page_view,name='page'),
    path('renovation/',views.renovation_view,name='renovation'),
    path('QandA/',views.qa_view,name='qa'),
    path('catalog/',views.catalog_view,name='catalog'),
    path('line/',views.line_view,name='contact_line')
]
