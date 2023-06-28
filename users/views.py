from django.shortcuts import render, redirect
from main.models import Member
import os
from django.conf import settings

# Create your views here.
def myPage(request):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    user = request.user
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        return render(request, "users/myPage.html")
        

    member = Member.objects.get(user=user)
    somds = member.somds.all()
    return render(request, "users/myPage.html", {
        'somds': somds,
    })

def myPage_edit(request):
    user = request.user

    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        return render(request, "users/myPage_edit.html")
        

    member = Member.objects.get(user=user)
    somds = member.somds.all()
    return render(request, "users/myPage_edit.html", {
        'somds': somds,
    })

def myPage_update(request):

    update_user = request.user

    if "profile_pic" in request.FILES:
        if update_user.profile.profile_pic:
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'user_profile/usrDefaultImage.png')
            if update_user.profile.profile_pic.path != default_image_path:
                os.remove(os.path.join(settings.MEDIA_ROOT, update_user.profile.profile_pic.path))
        update_user.profile.profile_pic = request.FILES["profile_pic"]
        
    # update_user.profile.name = request.POST['name']
    update_user.profile.nickname = request.POST['nickname']
    # update_user.profile.gender = request.POST['gender']
    # update_user.profile.birth = request.POST['birth']
    update_user.profile.intro= request.POST['intro']
    # update_user.profile.birth = f'{year}-{month}-{day}'
    update_user.profile.college = request.POST['college']
    update_user.profile.department = request.POST['department']
    # update_user.profile.email = request.POST['email']

    update_user.profile.save()
    update_user.save()

    return redirect('users:myPage')

