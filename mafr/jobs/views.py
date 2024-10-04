from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import JobForm, JobApplicationForm, JobApplicationStatusForm
from .models import Job, JobApplication


############################# JOB VIEWS ################################

@login_required
def create_job(request):
    if request.user.role == 'employer':
        if request.method == 'POST':
            form = JobForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.employer = request.user
                job.save()
                return redirect('get_jobs') 
        else:
            form = JobForm()

        return render(request, 'jobs/create_job.html', {'form': form})
    else:
        return HttpResponseForbidden("You are not allowed to create jobs.")  


# This view method is used by employers to get the list of the jobs they have created 
@login_required
def get_jobs(request):
    if request.user.role == 'employer':
        jobs = Job.objects.filter(employer=request.user.id)
        return render(request=request, template_name='jobs/jobs_list.html', context={'jobs': jobs})
    else:
        return render(request=request, template_name='404.html')

@login_required
def consult_job(request, job_id):

    if request.user.role == 'employer':
        job = Job.objects.get(id=job_id)
        return render(request=request, template_name='jobs/job_details.html', context={'job': job})
    
    else:
        return HttpResponseForbidden('Reserved for employers')

@login_required
def update_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.role == 'employer' and job.employer == request.user:
        if request.method == 'POST':
            form = JobForm(request.POST, instance=job)
            if form.is_valid():
                form.save()
                return render(request=request, template_name='jobs/job_details.html', context={'job': job})

        else:
            form = JobForm()

        return render(request=request, template_name='jobs/update_job.html', context={'form': form})
    
    else :
        return HttpResponseForbidden("Oh Wow :)")

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.role == 'employer' and job.employer == request.user:
        job.delete()
        return redirect('get_jobs')
    
    else : 
        return HttpResponseForbidden("Come on :=)")
    

@login_required
def track_job(request, job_id):

    if request.user.role == 'employer':

        # Get the job
        job = Job.objects.get(id=job_id)

        # Check if the user sending the request is the same the job owner
        if job.employer == request.user:
            
            # Get all applications to this job
            applications = JobApplication.objects.filter(job=job_id)

            return render(request=request, template_name='jobs/track_applications.html', context={'applications': applications})
        
        else: 

            return HttpResponseForbidden('Access Denied')
    
    else :

        return HttpResponseForbidden('Access Denied')
    

@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    # Ensure the user is the employer and owns the job
    if request.user.role == 'employer' and application.job.employer == request.user:
        if request.method == 'POST':
            form = JobApplicationStatusForm(request.POST, instance=application)
            if form.is_valid():
                form.save()
                return redirect('track_job', job_id=application.job.id)
        else:
            form = JobApplicationStatusForm(instance=application)

        return render(request, 'jobs/update_application_status.html', {'form': form, 'application': application})
    else:
        return HttpResponseForbidden('You are not authorized to update this application.')


############################# JOB_APPLICATION VIEWS ################################

# Get all posted offers (this route is accessible from both employers and talents)
@login_required
def get_all_offers(request):

    # Get all available offers
    offers = Job.objects.filter()

    return render(request=request, template_name='jobs/offers.html', context={'offers': offers})

@login_required
def get_offer(request, offer_id):

    # Get the offer
    offer = get_object_or_404(Job, id=offer_id)
    return render(request=request, template_name='jobs/offer_details.html', context={'offer': offer})



# Apply to offer
@login_required
def create_job_application(request, job_id):

    if request.user.role == 'talent':

        job = get_object_or_404(Job, id=job_id)

        if request.method == 'POST':
            form = JobApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                job_application = form.save(commit=False)
                job_application.job = job
                job_application.talent = request.user
                job_application.save()
                return redirect('my_applications')
        
        else:
            form = JobApplicationForm()
        
        return render(request=request, template_name='jobs/apply.html', context={'form': form, 'job': job})
    
    else :
        return HttpResponseForbidden("Only talents are authorized to apply :)")


@login_required
def get_all_job_applications(request):
    if request.user.role == 'talent':

        # Get applications associated with the current talent user
        myapplications = JobApplication.objects.filter(talent=request.user)

        if myapplications :
        
            return render(request=request, template_name='jobs/myapplications.html', context={'myapplications': myapplications})
        
        else :

            return HttpResponseForbidden("No results")

# Withdraw
@login_required
def cancel_job_application(request, application_id):

    # Get the job application
    job_application = JobApplication.objects.get(id=application_id)

    # Check if the request owner and job_app owner are the same, this allow users to cancel only their applications and not someone's app
    if request.user.role == 'talent' and request.user == job_application.talent :
        job_application.delete()
        return redirect('my_applications')
    
    else: 
        return HttpResponseForbidden("You don't have the authorization for this action")
