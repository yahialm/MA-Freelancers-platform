from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from profil.models import CustomUser
from .models import Project
from django import forms
from django.http import HttpResponseForbidden


###########################################   GET PROJECT(S)  ################################################

@login_required
def get_project(request, user_id, project_id):
    user = get_object_or_404(CustomUser, id=user_id)
    project = get_object_or_404(Project, user=user, id=project_id)
    
    if request.user.role == 'talent':
        is_owner = project.user == request.user
    else:
        is_owner = False
    
    return render(request, 'projects/project_detail.html', {'project': project, 'is_owner': is_owner})
        

@login_required
def get_all_projects(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    projects = Project.objects.filter(user=user)
    
    is_owner = request.user.role == 'talent' and request.user.id == user_id

    return render(request, 'projects/projects.html', {'projects': projects, 'is_owner': is_owner})
    
########################################## CREATE PROJECT ###################################################

# Project form
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'demo_link', 'github_link', 'technologies']

# This view allows only talents to add their own projects
@login_required
def create_project(request):
    if request.user.role != 'talent':
        return HttpResponseForbidden("Only talents can create projects.")

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('get_all_projects', user_id=request.user.id)
    else:
        form = ProjectForm()
    
    return render(request, 'projects/create_project.html', {'form': form, 'user_id': request.user.id})

############################################# Update project #########################################

@login_required
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.user.role != 'talent':
        return HttpResponseForbidden("Only talents can update projects.")
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return render(request, 'projects/project_detail.html', {'project': project})
    else:
        form = ProjectForm(instance=project)

    
    return render(request, 'projects/update_project.html', {'form': form, 'project_id': project.id, 'user_id': project.user.id})



############################################## Delete project #########################################

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.user.role != 'talent':
        return HttpResponseForbidden("Only talents can delete projects.")

    if request.method == 'POST':
        project.delete()
        return redirect('get_all_projects', user_id=request.user.id)

    return render(request, 'projects/delete_project_confirm.html', {'project': project})
