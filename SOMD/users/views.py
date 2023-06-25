from django.shortcuts import render, redirect
from main.models import Member

# Create your views here.
def mypage(request):
    user = request.user
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        return render(request, "users/mypage.html")
        

    member = Member.objects.get(user=user)
    somds = member.somds.all()
    return render(request, "users/mypage.html", {
        'somds': somds,
    })

def mypage_edit(request):
    user = request.user

    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        return render(request, "users/mypage_edit.html")
        

    member = Member.objects.get(user=user)
    somds = member.somds.all()
    return render(request, "users/mypage_edit.html", {
        'somds': somds,
    })

def mypage_update(request):

    update_user = request.user

    if "profile_pic" in request.FILES:
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

    return redirect('users:mypage')

