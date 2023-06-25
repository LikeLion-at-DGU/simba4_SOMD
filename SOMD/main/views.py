from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count 
from .models import Post, Comment, Tag, SOMD, Member, Images, JoinRequest
from django.contrib.auth.models import User
from django.utils import timezone
import re
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Create your views here.


def mainpage(request):
    if request.user.is_authenticated:
        user = request.user
        members = Member.objects.filter(user=user)
        somds = SOMD.objects.filter(members__in=members)
        if somds:
            return render(request, 'main/mainpage.html', {'somds': somds})
    return render(request, 'main/mainpage.html')

    
def board(request):
    somds = SOMD.objects.all()
    tags = Tag.objects.all()
    return render(request, 'main/board.html', {
        "somds": somds,
        "tags": tags,
    })


def register(request):
    tags = Tag.objects.all()
    return render(request,'main/register.html',{
        "tags":tags,
    })

def createSOMD(request):
    if request.user.is_authenticated:
        user = request.user
        new_somd = SOMD()
        if "back_pic" in request.FILES:
            new_somd.backgroundimage = request.FILES["back_pic"]
        
        
        if "profile_pic" in request.FILES:
            new_somd.profileimage = request.FILES["profile_pic"]
        
    
        new_somd.name = request.POST["somdname"]

        new_somd.department = request.POST["department"]
        new_somd.college = request.POST["college"]

        # new_somd.category = request.POST["category"]
        new_somd.intro = request.POST["intro"]
        new_somd.snslink = request.POST["snslink"]
        new_somd.admin = request.user
        new_somd.save()

        tags = request.POST.getlist("tags")  # 선택된 태그 텍스트
        for tag in tags :
            tag, created = Tag.objects.get_or_create(name=tag)
            new_somd.tags.add(tag)

        member, created = Member.objects.get_or_create(user=user)
        member.somds.add(new_somd)
        # new_somd.admins.set([request.user])
        
        new_somd.join_members.add(request.user)
        
        return redirect("main:mainfeed", new_somd.id)
    else:
        return redirect('accounts:login')

def somd_edit(request, id):

    somd = SOMD.objects.get(id=id)
    tags = Tag.objects.all()

    return render(request, "main/somd_edit.html", {
            'somd': somd,
            'tags' : tags,
    })

def somd_update(request, id):
    update_somd =  SOMD.objects.get(id=id)
    
    if "back_pic" in request.FILES:
        update_somd.backgroundimage = request.FILES["back_pic"]
    

    if "profile_pic" in request.FILES:
        update_somd.profileimage = request.FILES["profile_pic"]
   

    update_somd.name = request.POST["somdname"]

    update_somd.department = request.POST["department"]
    update_somd.college = request.POST["college"]


    # update_somd.category = request.POST["category"]
    update_somd.intro = request.POST["intro"]
    update_somd.snslink = request.POST["snslink"]
    update_somd.admin = request.user

    tags = request.POST.getlist("tags")  # 선택된 태그 텍스트
    for tag in update_somd.tags.all() :
        update_somd.tags.remove(tag)

    for tag in tags :
        tag, created = Tag.objects.get_or_create(name=tag)
        update_somd.tags.add(tag)


    update_somd.save()
    return redirect("main:mainfeed", update_somd.id)


def mainfeed(request, id):
    somd = SOMD.objects.get(id=id)
    posts = somd.somds.filter(is_fixed=False)
    fixed_posts = somd.somds.filter(is_fixed=True)

    return render(request, "main/mainfeed.html", {
        'somd': somd,
        'posts': posts,
        'fixed_posts': fixed_posts,
    })
# def mainfeed(request, id):
#     # user = request.user
#     # member = Member.objects.get(user=user)
#     somd = SOMD.objects.get(id=id)
#     posts = somd.somds.all()
#     return render(request, "main/mainfeed.html", {
#         'somd': somd,
#         'posts':posts
#     })

def mysomd(request):
    user = request.user
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        return render(request, "main/mysomd.html")
        
    member = Member.objects.get(user=user)
    somds = member.somds.all()
    # tags = Tag.objects.all()

    waiting_somds = member.waiting_somds.all()
    return render(request, "main/mysomd.html", {
        'somds': somds,
        'waiting_somds':waiting_somds,
        # 'tags':tags,
    })
    
def new(request,somd_id):
    somd = SOMD.objects.get(id=somd_id)
    return render(request, 'main/new.html', {'somd': somd})

def createpost(request, somd_id):
    # if request.user in SOMD.members:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content', '')
            writer = request.user
            somd = SOMD.objects.get(id=somd_id)

            new_post = Post.objects.create(
                title=title,
                writer=writer,
                pub_date=timezone.now(),
                content=content,
                somd=somd
            )

            images = request.FILES.getlist('images')
            for image in images:
                new_image = Images.objects.create(post=new_post, image=image)

            return render(request, 'main/viewpost.html', {'post': new_post, 'images': new_post.images.all()})


def join(request, id):
    somd = SOMD.objects.get(id=id)
    return render(request, "main/join.html", {
        'somd': somd,
    })


def wantTojoin(request, id):
    somd = SOMD.objects.get(id=id)

    new_join_request = JoinRequest()

    if request.method == 'POST':
        new_join_request.writer = (request.user)

        new_join_request.title = request.POST.get('title')
        new_join_request.motivation = request.POST.get('motivation')
        new_join_request.pub_date = timezone.now()
        
        new_join_request.save()
    
    member, created = Member.objects.get_or_create(user=request.user)
    member.waiting_somds.add(somd)

    somd.waitTojoin_members.add(request.user)
    somd.join_requests.add(new_join_request)

    return redirect("main:mainfeed", somd.id)


def members(request, id):
    somd = somd = SOMD.objects.get(id=id)
    
    return render(request, "main/members.html", {
        'somd': somd,
    })

def members_wantTojoin(request, somd_id, request_id):
    somd = SOMD.objects.get(id=somd_id)
    joinrequest = JoinRequest.objects.get(id=request_id)

    member = Member.objects.get(user = joinrequest.writer)

    if request.method == 'POST':
        if "accept" == request.POST["wantTojoin_result"] :
            somd.join_members.add(joinrequest.writer)
            somd.waitTojoin_members.remove(joinrequest.writer)
            member.somds.add(somd)
            
        elif "reject" == request.POST["wantTojoin_result"] :
            somd.waitTojoin_members.remove(joinrequest.writer)
            member.rejected_somds.add(somd)

        somd.join_requests.remove(joinrequest)
        joinrequest.delete()

        member.waiting_somds.remove(somd)

    return render(request, "main/members.html", {
        'somd': somd,
    })


def members_delete(request, somd_id, join_user_id):
    somd = SOMD.objects.get(id=somd_id)
    join_user = User.objects.get(id=join_user_id)
    member = Member.objects.get(user = join_user)

    member.somds.remove(somd)
    somd.join_members.remove(join_user)
    member.rejected_somds.add(somd)

    return render(request, "main/members.html", {
        'somd': somd,
    })


def viewpost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'GET':
        images = post.images.all()
        comments = Comment.objects.filter(post=post)
        num_likes = post.like.count()
        return render(request, 'main/viewpost.html', {
            'post': post,
            'images': images,
            'comments': comments,
            'num_likes': num_likes,
        })
    elif request.method == 'POST':
        if request.user.is_authenticated:
            new_comment = Comment()
            new_comment.post = post
            new_comment.writer = request.user
            new_comment.content = request.POST["comment"]
            new_comment.pub_date = timezone.now()
            new_comment.save()
            # post.comment.count()
            # post.update_num_comments()

            return redirect('main:viewpost', post.id)

def bookmark(request,SOMD_id):
    bookmarked_somd = get_object_or_404(SOMD, pk=id)
    user = request.user
    is_user_bookmarked = user.bookmark.filter(id=bookmarked_somd.id).exists()
    
    if is_user_bookmarked:
        user.bookmark.add(bookmarked_somd) 
        bookmarked = True
    
    else:
        user.bookmark.remove(bookmarked_somd)
        bookmarked = False
        
    return redirect('main:mysomd', bookmarked_somd.id) #??어디로 redirect??



    
    
def Scrap(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    is_user_scraped = user.scrap.filter(id=post.id).exists()
    
    if is_user_scraped:
        user.scrap.add(post) 
        scraped = True
    
    else:
        user.scrap.remove(post)
        scraped = False
        
    return redirect('main:viewpost', post.id)


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user.is_authenticated:
        if post.like.filter(id=user.id).exists():
            post.like.remove(user)
        else:
            post.like.add(user)
    return redirect('main:viewpost', post_id)


def CountSomdMember(request):
    somds = SOMD.objects.annotate(num_members=Count('members')).all()
    return render(request, 'main/board.html', {"somds": somds})

# def JoinRequest(request):
#         new_join_request = JoinRequest()
#         user = request.user.profile 
#         created_at = timezone.now()
#         title = request.POST.get('title')
#         motivation = request.POST.get('motivation')
        
#         new_join_request.save()
        
        
#         join_request = JoinRequest(user=user, title=title, motivation=motivation)
#         join_request.save()  
        
#         return redirect('가입완료페이지')

def fix(request, post_id, somd_id):
    post = get_object_or_404(Post, id=post_id)
    if post.is_fixed:
        post.is_fixed = False
    else:
        post.is_fixed = True
    post.save()
    
    return redirect('main:mainfeed', id = somd_id)
