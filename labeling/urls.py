from django.conf.urls import url
from django.contrib.auth import views as auth_views
# from . import views
from views import *

urlpatterns = [
	url(r'^$', IndexPage.as_view()),
	url(r'^index/$', IndexPage.as_view(), name='index'),
    url(r'^project_actions/$', ProjectActionsPage.as_view(), name='project_actions'),
    # url(r'^project_actions/(?P<success>[a-zA-Z]+)/$', ProjectActionsPage.as_view(), name='project_actions'),
    url(r'^project_actions/(?P<success>[0-9]+)/$', ProjectActionsPage.as_view(), name='project_actions'),
    url(r'^create_project/$', CreateProjectPage.as_view(), name='create_project'),
    url(r'^existing_projects/$', ExistingProjectsPage.as_view(), name='existing_projects'),
    url(r'^workers_hits/$', WorkersHitsPage.as_view(), name='workers_hits'),
    url(r'^ulogin/$', auth_views.login, {'template_name': 'userreg/home.html'}, name='login'),
    url(r'^ulogout/$', auth_views.logout, {'template_name': 'userreg/logged_out.html'}, name='logout'),
    url(r'^register/$', RegistrationPage.as_view(), name='register'),
    url(r'^display_hit_tuples/$', DisplayHitTuplesPage.as_view(), name='display_hit_tuples'),
    url(r'^display_hit_tuples/(?P<project_id>[0-9]+)/$', DisplayHitTuplesPage.as_view(), name='display_hit_tuples'),
    url(r'labeling_service/(?P<assignment_id>[0-9]+)/$',
        LabelingServicePage.as_view(), name='labeling_service'),
    url(r'^view_project/(?P<project_id>[0-9]+)/$', ViewProjectPage.as_view(), name='view_project'),
    url(r'^view_hit/(?P<hit_id>[0-9]+)/$', ViewHitPage.as_view(), name='view_hit'),
    url(r'^completion_notice/$', CompletionNoticePage.as_view(), name='completion_notice'),
    url(r'^completion_notice/(?P<assignment_id>[0-9]+)/$', CompletionNoticePage.as_view(), name='completion_notice'),

    url(r'^edit_project_parameters/$', EditProjectParametersPage.as_view(), name='edit_project_parameters'),

    url(r'^edit_project_parameters/(?P<project_id>[0-9]+)/$', EditProjectParametersPage.as_view(), name='edit_project_parameters'),
    url(r'^review_labelling/$', ReviewLabellingPage.as_view(), name='review_labelling'),
    url(r'^delete_project/(?P<delete_project_id>[0-9]+)/$', DeleteProjectPage.as_view(), name='delete_project'),
    
]
