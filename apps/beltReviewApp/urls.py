from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index), #display login
    url(r'^login$', views.login), #process login form
    url(r'^register$', views.register), #display registration
    url(r'^process$', views.process), #process registration form
    url(r'^books$', views.books), #display books
    url(r'^books/(?P<number>[0-9])$', views.bookDisplay), #display book info page
    url(r'^users/(?P<number>[0-9])$', views.user), #display user info page
    url(r'^users/(?P<number>[0-9])/update$', views.update), #display update user info page
    url(r'^update/(?P<number>[0-9])$', views.userUpdate), #process user update form info
    url(r'^users/(?P<number>[0-9])/delete$', views.deleteUser), #display delete user info page
    url(r'^add$', views.add), #display add book
    url(r'^check$', views.check), #process add book form
    url(r'^books/(?P<number>[0-9])/review$', views.review),
    url(r'^books/(?P<number>[0-9])/delete$', views.delete),
    url(r'^logout$', views.logout), #logout
]