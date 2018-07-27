from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$' , views.index),
    # url(r'^$' , views.dashboard),
    url(r'^addJob$' , views.addJob),
    url(r'^addJob_render$' , views.addJob_render),
    url(r'^createJob$' , views.createJob),
    url(r'^dashboard$' , views.dashboard),
    # for login and registration
    
    url(r'^login$' , views.login),
    url(r'^register$' , views.register),
    url(r'^logout$' , views.logout),
    # functions
    url(r'^edit/(?P<job_id>\d+)$' , views.edit ),
    url(r'^editJob/(?P<job_id>\d+)$' , views.editJob ),
    url(r'^back$' , views.back ),
    url(r'^add/(?P<job_id>\d+)$' , views.add ),
    url(r'^view/(?P<job_id>\d+)$' , views.view ),
    url(r'^cancel/(?P<job_id>\d+)$' , views.cancel ),
    url(r'^done/(?P<job_id>\d+)$' , views.done ),
]