from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm


# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                # print("user takend")
                messages.error(request, "Username taken")
                return redirect('regapp:signup')
            elif User.objects.filter(email=email).exists():
                # print("email taken")
                messages.info(request, "email taken")
                return redirect('regapp:signup')
            else:
                user = User.objects.create_user(username=username, password=cpassword, email=email,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save();
                return redirect('regapp:login')
        else:
            # print("password not match")
            messages.info(request, "password is not match")

    return render(request, "signup.html")


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('movies:movie_list')
        else:
            messages.error(request, 'invalid credentials.Try again')
            return redirect('regapp:login')
    return render(request, 'login.html')

@login_required

def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out.")  # Optional: Display a logout message
    # return redirect('regapp:login')
    return render(request, 'login.html')

@login_required
def view_profile(request):
    profile = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    # profile = UserProfile.objects.get_or_create(user=request.user)
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('regapp:view_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})
