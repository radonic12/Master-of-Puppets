from django.conf.urls import url
from . import views
# Create your views here.

urlpatterns = [
    #signout
    url(r'api', views.api, name='api'),
    #signout
    url(r'signout', views.signout, name='signout'),
    #Add existing unqkey to user profil
    url(r'addExst', views.addExst, name='addExst'),
    #Url for associate your user profil with an unique key
    url(r'userKey', views.usrKey, name='usrKey'),
    #Url for signing in
    url(r'login', views.login, name='login'),
    #Url for updating feature
    url(r'updFeat', views.updFeat, name='updFeat'),
    #Url for deleting feature
    url(r'dltFeat', views.dltFeat, name='dltFeat'),
    #Url for creating feature
    url(r'addFeat', views.addFeat, name='addFeat'),
    #Url for creating unique string
    url(r'unqcrt', views.unq, name='unq'),
    #Url for control panel
    url(r'workon', views.wrkon, name='wrkon'),
    #Url for frontpage
    url(r'', views.indx, name='indx'),

]