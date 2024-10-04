from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserRegistrationForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TalentProfile, EmployerProfile, CustomUser


############################## Register ######################################

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        user_role = request.POST.get('role')
        print(user_role)

        if form.is_valid():
            user = form.save()

            login(request=request, user=user)

            if user_role == 'talent':
                # Redirect the user to create his profile as talent
                # The user should give infos linked to talent_profile 
                # Then we should save the infos of the talent + associate 
                # to ths user currently submitting the form
                return redirect('complete_talent_profile')
            
            elif user_role == 'employer':
                # Redirect the user to create his employer as talent
                # The user should give infos linked to emp_profile 
                # Then we should save the infos of the employer + associate 
                # to ths user currently submitting the form
                return redirect('complete_employer_profile')
    
    else:
        form = CustomUserRegistrationForm()
    
    return render(request, "profil/register.html", {'form': form})

##########################  Profile Completion ############################

class TalentProfileForm(forms.ModelForm):
    class Meta:
        model = TalentProfile
        fields = ['specialization', 'github_url', 'linkedin_url']

@login_required
def complete_talent_profile(request):
    if request.method == 'POST':
        form = TalentProfileForm(request.POST)
        if form.is_valid():
            talent_profile = form.save(commit=False)
            # Associate the profile with the current user
            talent_profile.user = request.user
            talent_profile.save()
            return redirect('home')
    else:
        form = TalentProfileForm()

    return render(request, 'profil/complete_talent_profile.html', {'form': form})

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_website', 'linkedin_url']

@login_required
def complete_employer_profile(request):
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST)
        if form.is_valid():
            employer_profile = form.save(commit=False)
            employer_profile.user = request.user
            employer_profile.save()
            return redirect('home')
    else:
        form = EmployerProfileForm()

    return render(request, 'profil/complete_employer_profile.html', {'form': form})


########################## Login/Logout ###############################

# Login view
def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('get_jobs')
    else:
        form = AuthenticationForm()
    
    return render(request, 'profil/login.html', {'form': form})


# Logout view
def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('home')  # Redirect to the homepage


############################# Profile #####################################

# Get profile informations of the user
@login_required
def visit_profile(request, user_id):

    user = get_object_or_404(CustomUser, id=user_id)
    is_owner = request.user.id == user_id
    
    # Determine if the user is a talent or employer
    if user.role == 'talent':
        profile = get_object_or_404(TalentProfile, user=user)
        template_name = 'profil/talent_profile.html'
    elif user.role == 'employer':
        profile = get_object_or_404(EmployerProfile, user=user)
        template_name = 'profil/employer_profile.html'
    
    return render(request, template_name, {'profile': profile, 'user': user, 'is_owner': is_owner})


# Current user profile details
def myprofile(request):

    current_user = request.user
    print("-->", current_user.role)

    if current_user.role == 'talent':
        current_talent_profile = get_object_or_404(TalentProfile, user=current_user)
        return render(request, 'profil/myprofile_talent.html', {
            'profile': current_talent_profile
        })
    elif current_user.role == 'employer':
        current_employer_profile = get_object_or_404(EmployerProfile, user=current_user)
        return render(request, 'profil/myprofile_employer.html', {
            'profile': current_employer_profile
        })
    else:
        # Handle the case if the role is neither 'talent' nor 'employer'
        return render(request, '404.html', {
            'message': 'User role not recognized'
        })


#########################################################
def home(request):
    return render(request, 'home.html')