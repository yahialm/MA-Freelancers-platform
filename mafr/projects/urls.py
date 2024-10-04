from django.urls import path
from . import views

urlpatterns = [

    path(route='profile/<int:user_id>/project/<uuid:project_id>', view=views.get_project, name='get_project'),
    path(route='profile/<int:user_id>/projects', view=views.get_all_projects, name='get_all_projects'),
    path(route='profile/project/new', view=views.create_project, name='create_project'),
    path(route='profile/project/<uuid:project_id>/update', view=views.update_project, name='update_project'),
    path(route='profile/project/<uuid:project_id>/delete', view=views.delete_project, name='delete_project'),

]
