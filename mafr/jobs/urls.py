from django.urls import path
from . import views


urlpatterns = [

    # Get a specific/all job(s) - This route is accessible for all users
    # This view should get the user to specific job informations
    # The template should handle if a user is talent or employer
    # TODO: If the user is a talent we need to display 'Apply' and 'Withdraw' buttons {{{DONE}}}
    # TODO: If the user is an employer we need to display 'Update' and 'Delete'  {{{DONE}}}
    path(route='myprofile/jobs/<int:job_id>', view=views.consult_job, name='consult_job'),
    path(route='myprofile/jobs/posted', view=views.get_jobs, name='get_jobs'),
    path(route='myprofile/jobs/<int:job_id>/applications_received', view=views.track_job, name='track_job'),
    path(route='myprofile/jobs/<int:application_id>/update-status/', view=views.update_application_status, name='update_application_status'),
    
    # Only employers should be able to post new offers, Update and delete them, and for sure they can see them
    path(route='jobs/new', view=views.create_job, name='create_job'),
    path(route='jobs/<int:job_id>/update', view= views.update_job, name='update_job'),
    path(route='jobs/<int:job_id>/delete', view=views.delete_job, name='delete_job'),
    # TODO: path(route='jobs/repost', view=views.repost_job, name='repost_job')



    # Talents shouldn't be able to CRUD new job offers, but only they can apply so they can track their applications and also cancel them if they want

    # This routes are public and accessible for both talents and employers
    path(route='offers/', view=views.get_all_offers, name='get_all_offers'),
    path(route='offer/<int:offer_id>', view=views.get_offer, name='get_offer'),



    # Apply to job offers
    path(route='offer/<int:job_id>/apply', view=views.create_job_application, name='create_job_application'),

    # Cancel job applications
    path(route='offer/<int:application_id>/cancel', view=views.cancel_job_application, name='cancel_job_application'),

    # Users can see their job applications
    path(route='myapplications', view=views.get_all_job_applications, name='my_applications'),
]