from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, F, ExpressionWrapper, FloatField
from .models import Post, Comment, Tag, SOMD, Member, Images, JoinRequest, UserAlram, Alram
from django.contrib.auth.models import User
from django.utils import timezone
import re
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# 비동기 좋아요를 위해 추가한 django.http
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

def start(request):
    return render(request,'main/start.html')

def mainPage(request):
    if request.user.is_authenticated:
        user = request.user
        members = Member.objects.filter(user=user)
        somds = SOMD.objects.filter(members__in=members)

        alrams, created = UserAlram.objects.get_or_create(user=user)

    

        posts = Post.objects.filter(somd__in =somds)
        if somds:
            posts = posts.order_by('-pub_date')
            return render(request, 'main/mainPage.html', {
                'somds': somds,
                'posts' : posts,

                'alrams':alrams,
                
            })
    return render(request, 'main/mainPage.html')



def somdList(request):
    #somds = SOMD.objects.all()
    #rank_somds = SOMD.objects.annotate(totalMember=Count('members'), totalPosts=Count('posts'), ratio='totalPosts'/'totalMember').filter(totalMember__gte=5).order_by('-totalMember', '-totalPosts')[:7]
    rank_somds = SOMD.objects.annotate(
        totalMember=Count('members'),
        totalPosts=Count('posts'),
        ratio=ExpressionWrapper(F('totalPosts') / F('totalMember'), output_field=FloatField())
        ).filter(totalMember__gte=5).order_by('-ratio')[:7]
    tags = Tag.objects.all()
    somds = SOMD.objects.all()
        
    return render(request, 'main/somdList.html', {
        "rank_somds": rank_somds,
        "tags": tags,
        "somds": somds,
    })


def somd_new(request):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    tags = Tag.objects.all()
    return render(request,'main/somd_new.html',{
        "tags":tags,
    })

def somd_create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    if request.user.is_authenticated:
        user = request.user
        new_somd = SOMD()

        if "back_pic" in request.FILES:
            new_somd.backgroundimage = request.FILES["back_pic"]
            new_somd.filename_back = request.FILES["back_pic"].name
        
        if "profile_pic" in request.FILES:
            new_somd.profileimage = request.FILES["profile_pic"]
            new_somd.filename_prof = request.FILES["profile_pic"].name
        
    
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
        
        return redirect("main:somdFeed", new_somd.id)
    else:
        return redirect('accounts:needTologin')

def somd_edit(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    somd = SOMD.objects.get(id=id)
    tags = Tag.objects.all()

    return render(request, "main/somd_edit.html", {
            'somd': somd,
            'tags' : tags,
    })

def somd_update(request, id):
    
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    update_somd =  SOMD.objects.get(id=id)
    
    if "back_pic" in request.FILES:
        if update_somd.backgroundimage:
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'somd/somdbackDefaultImage.png')
            if update_somd.backgroundimage.path != default_image_path:
                os.remove(os.path.join(settings.MEDIA_ROOT, update_somd.backgroundimage.path))
        update_somd.backgroundimage = request.FILES["back_pic"]


    if "profile_pic" in request.FILES:
        if update_somd.profileimage:
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'somd/somdDefaultImage.png')
            if update_somd.profileimage.path != default_image_path:
                os.remove(os.path.join(settings.MEDIA_ROOT, update_somd.profileimage.path))
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
    return redirect("main:somdFeed", update_somd.id)


def somdFeed(request, id):
    if request.method == "POST":
        option_state = request.POST['option_state']
    else:
        option_state= "리스트"

    somd = SOMD.objects.get(id=id)
    user = request.user
    # 소모임 가입 여부 확인
    is_member = somd.join_members.filter(id=user.id).exists()
    # posts : 가입자 - 고정글 제외 / 미가입자 - 고정글, 비밀글 제외
    posts = somd.posts.filter(is_fixed=False) if is_member else somd.posts.filter(is_fixed=False, is_secret=False)
    # fixed_posts : 가입자, 미가입자 모두 고정글에 접근 가능
    fixed_posts = somd.posts.filter(is_fixed=True)
    # 이하 동일
    # image_fixed_posts = fixed_posts.filter(images__isnull=False)
    # image_posts = posts.filter(images__isnull=False)

    if(option_state == "피드"):
        posts = posts.filter(images__isnull =False)
        fixed_posts = fixed_posts.filter(images__isnull =False)
        if posts.count() == 0:
            num_per_page =1
        else :
            num_per_page = posts.count()

    else:
        num_per_page = 6

    page_obj = page_list(request,posts,num_per_page)
    # page_obj1, custom_range1 = page_list(request,image_posts,num_per_page)
    

    return render(request, "main/somdFeed.html", {
        # 'image_fixed_posts': image_fixed_posts,
        # 'image_posts': image_posts,
        'somd': somd,
        'fixed_posts': fixed_posts,
        'posts': page_obj,
        'page_obj': page_obj,
        #'custom_range': custom_range,
        # 'page_obj1': page_obj1,
        # 'custom_range1': custom_range1,
        'option_state': option_state,
    })




def mySomd(request):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    user = request.user
    alrams, created = UserAlram.objects.get_or_create(user=user)

    member, created = Member.objects.get_or_create(user=user)

    somds = member.somds.all()
    # tags = Tag.objects.all()
    
    waiting_somds = member.waiting_somds.all()
    return render(request, "main/mySomd.html", {
        'somds': somds,
        'waiting_somds':waiting_somds,
        'alrams':alrams,
        # 'tags':tags,
    })
    
def somd_post_new(request,somd_id):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    somd = SOMD.objects.get(id=somd_id)
    return render(request, 'main/somd_post_create.html', {'somd': somd})

def somd_post_create(request, somd_id):
    
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    # if request.user in SOMD.members:
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content', '')
        writer = request.user
        somd = SOMD.objects.get(id=somd_id)
        
        if(request.POST.get('is_secret')=="0"):
            is_secret = False
        else:
            is_secret = True

        new_post = Post.objects.create(
            title=title,
            writer=writer,
            pub_date=timezone.now(),
            content=content,
            somd=somd,

            is_secret = is_secret
        )
        
        if request.FILES.getlist('images'):
            for image in request.FILES.getlist('images'):
                filename = image.name
                new_image = Images.objects.create(post=new_post, image=image, filename=filename)


        # images = request.FILES.getlist('images')
        # for image in images:
        #     new_image = Images.objects.create(post=new_post, image=image, filename=image.filename)
        
        return redirect("main:somd_post_view", new_post.id)


def join(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    somd = SOMD.objects.get(id=id)
    return render(request, "main/join.html", {
        'somd': somd,
    })


def wantTojoin(request, id):
    
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
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

    #유저에게 알람 전달
    receiveUser, created = UserAlram.objects.get_or_create(user=somd.admin)

    receiveUser.new = True
    receiveUser.save()
    
    alram = Alram()
    alram.type ="userJoin"
    alram.sendUser = (request.user)
    alram.somd = (somd)
    alram.date = timezone.now()

    alram.save()

    receiveUser.alrams.add(alram)

    return redirect("main:somdFeed", somd.id)


def somd_members(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    somd = somd = SOMD.objects.get(id=id)
    
    return render(request, "main/somd_members.html", {
        'somd': somd,
    })

def your_view(request):
    if request.user == post.writer:

        # post.writer와 post.writer.profile.profile_pic.url 값이 올바른지 확인
        print(post.writer)
        print(post.writer.profile.profile_pic.url)

        # 템플릿 변수를 전달
        context = {
            'post': post,
        }

    return render(request, 'your_template.html', context)



def somd_members_wantTojoin(request, somd_id, request_id):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    somd = SOMD.objects.get(id=somd_id)
    joinrequest = JoinRequest.objects.get(id=request_id)

    member = Member.objects.get(user = joinrequest.writer)

    if request.method == 'POST':
        if "accept" == request.POST["wantTojoin_result"] :
            somd.join_members.add(joinrequest.writer)
            somd.waitTojoin_members.remove(joinrequest.writer)
            member.somds.add(somd)

            receiveUser, created = UserAlram.objects.get_or_create(user=joinrequest.writer)
            
            receiveUser.new = True
            receiveUser.save()
            
            alram = Alram()
            alram.type ="somdAccept"
            alram.sendUser = (request.user)
            alram.somd = (somd)
            alram.date = timezone.now()

            alram.save()

            receiveUser.alrams.add(alram)
            
        elif "reject" == request.POST["wantTojoin_result"] :
            somd.waitTojoin_members.remove(joinrequest.writer)
            member.rejected_somds.add(somd)

            #유저에게 알람 전달
            receiveUser, created = UserAlram.objects.get_or_create(user=joinrequest.writer)

            receiveUser.new = True
            receiveUser.save()
            
            alram = Alram()
            alram.type ="somdReject"
            alram.sendUser = (request.user)
            alram.somd = (somd)
            alram.date = timezone.now()

            alram.save()

            receiveUser.alrams.add(alram)



        somd.join_requests.remove(joinrequest)
        joinrequest.delete()

        member.waiting_somds.remove(somd)

    return redirect("main:somd_members", somd.id)


def somd_members_delete(request, somd_id, join_user_id):
    
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    somd = SOMD.objects.get(id=somd_id)
    join_user = User.objects.get(id=join_user_id)
    member = Member.objects.get(user = join_user)

    if request.user == somd.admin:
        if request.user != join_user:
            somd.join_members.remove(join_user)
            member.somds.remove(somd)
            member.rejected_somds.add(somd)
        

            #유저에게 알람 전달
            receiveUser, created = UserAlram.objects.get_or_create(user=join_user)

            receiveUser.new = True
            receiveUser.save()
                
            alram = Alram()
            alram.type ="userDelete"
            alram.sendUser = (request.user)
            alram.somd = (somd)
            alram.date = timezone.now()

            alram.save()

            receiveUser.alrams.add(alram)

            return redirect("main:somd_members", somd.id)
        else:
            return redirect("main:somd_members", somd.id)


def somd_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'GET':
        images = post.images.all()
        comments = Comment.objects.filter(post=post)
        
        return render(request, 'main/somd_post_view.html', {
            'post': post,
            'images': images,
            'comments': comments,
        })
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:needTologin')

        if request.user.is_authenticated:
            new_comment = Comment()
            new_comment.post = post
            new_comment.writer = request.user
            new_comment.content = request.POST["comment"]
            new_comment.pub_date = timezone.now()
            new_comment.save()
            post.comment_count += 1
            post.save()

            return redirect('main:somd_post_view', post.id)

def bookmark(request, somd_id):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    somd = SOMD.objects.get(id=somd_id)
    user = request.user
    is_user_bookmarked = user.bookmark.filter(id=somd.id).exists()

    if is_user_bookmarked:
        user.bookmark.remove(somd)
        is_user_bookmarked = False
    else:
        user.bookmark.add(somd)
        is_user_bookmarked = True

    user.save()

    return redirect('main:somdFeed', somd.id)


def scrap(request, post_id):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    is_user_scraped = user.scrap.filter(id=post.id).exists()
    
    if is_user_scraped:
        user.scrap.remove(post) 
    else:
        user.scrap.add(post)
    user.save()
    return redirect('main:somd_post_view', post.id)

def scrap_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    user = request.user
    posts = user.scrap.all()
    return render(request, 'main/scrappedPost_view.html', {'posts':posts})


# def somd_post_like(request, post_id):
#     if not request.user.is_authenticated:
#         return redirect('accounts:needTologin')
    
#     post = get_object_or_404(Post, id=post_id)
#     user = request.user
#     if user in post.like.all():
#         post.like.remove(request.user)
#         post.like_count -= 1
#     else:
#         post.like.add(request.user)
#         post.like_count += 1
#     post.save()
#     return redirect('main:somd_post_view', post_id)

def somd_post_like(request, post_id):
    # if not request.user.is_authenticated:
    #     return redirect('accounts:needTologin')
    if not request.user.is_authenticated:
        return JsonResponse({'alert': '로그인이 필요합니다.'})

    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.like.all():
        post.like.remove(user)
        post.like_count -= 1
        liked = False
    else:
        post.like.add(user)
        post.like_count += 1
        liked = True
    post.save()
    
    return JsonResponse({'like_count': post.like_count, 'liked': liked})




# def CountSomdMember(request):
#     somds = SOMD.objects.annotate(num_members=Count('members')).all()
#     return render(request, 'main/somdList.html', {"somds": somds})

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
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    somd = get_object_or_404(SOMD, id=somd_id)
    post = get_object_or_404(Post, id=post_id)

    fixed_posts_count = Post.objects.filter(somd=somd, is_fixed=True).count()

    if somd.admin == request.user:
        if fixed_posts_count >= 2:
            if post.is_fixed:
                post.is_fixed = False
                post.save()
            else:
                return redirect('main:somdFeed', id = somd_id)
        else:
            post.is_fixed = True
            post.save()
    
    return redirect('main:somdFeed', id = somd_id)

def alram(request):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    alrams, created = UserAlram.objects.get_or_create(user=request.user)
    alrams.new = False
    alrams.save()

    return render(request, "main/alram.html", {
        'alrams': alrams,
    })

def somd_post_edit(request, post_id):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    edit_post = Post.objects.get(id=post_id)
    return render(request, "main/somd_post_update.html", {"post": edit_post})

def somd_post_update(request, post_id):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    user = request.user
    update_post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        if user == update_post.writer:
            if(request.POST.get('is_secret')=="0"):
                is_secret = False
            else:
                is_secret = True
            update_post.title = request.POST['title']
            update_post.content = request.POST['content']
            update_post.pub_date = timezone.now()

            update_post.is_secret = is_secret

            if request.FILES.getlist('images'):
                for image in update_post.images.all():
                    if image.image:
                        os.remove(os.path.join(settings.MEDIA_ROOT, image.image.path))
                    
                update_post.images.all().delete()
                images = request.FILES.getlist('images')
                for image in images:
                    filename = image.name
                    new_image = Images.objects.create(post=update_post, image=image, filename=filename)
            
            update_post.save()
            return redirect('main:somd_post_view', post_id)
    return redirect('main:somd_post_view', post_id)


def somd_post_delete(request, post_id):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.writer:
        for image in post.images.all():
            if image.image:
                image.image.delete()
        post.delete()
    return redirect('main:somdFeed', post.somd.id)

def comment_update(request, post_id, comment_id):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    post = get_object_or_404(Post, id=post_id)
    update_comment = get_object_or_404(Comment, id=comment_id)
    user = request.user
    if request.method == 'POST':
        if update_comment.writer == user:
            update_comment.post = post
            update_comment.content = request.POST['content']
            update_comment.pub_date = timezone.now()
            update_comment.save()
            return redirect('main:somd_post_view', update_comment.post.id)
    return render(request, 'main/somd_post_view.html', {'post': update_comment.post})

def comment_delete(request, post_id, comment_id):
    if not request.user.is_authenticated:
        return redirect('accounts:needTologin')
    
    post = get_object_or_404(Post, id=post_id)
    delete_comment = get_object_or_404(Comment, id=comment_id)
    if request.user == delete_comment.writer:
        post.comment_count -= 1
        delete_comment.delete()
        post.save()
    return redirect('main:somd_post_view', post.id)

def page_list(request, posts_list, num_per_page):
    paginator = Paginator(posts_list, num_per_page)
    page_num = request.GET.get('page')  # 현재 페이지 번호
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:            # url로 intger 값 아닌 값이 넘어올 때
        page_num = 1                    # 페이지를 1로 설정
        page_obj = paginator.page(page_num)
    except EmptyPage:                   # 해당 페이지에 개체가 없을 때
        page_num = paginator.num_pages  # 페이지를 마지막 페이지로 설정
        page_obj = paginator.page(page_num)

    # left_index = int(page_num) - 2      # 현재 페이지 기준으로 왼쪽에 보여줄 페이지 개수
    # if left_index < 1:                  # 왼쪽에 보여줄 페이지 개수가 1보다 작으면 1로 설정
    #     left_index = 1

    # right_index = int(page_num) + 2     # 현재 페이지 기준으로 오른쪽에 보여줄 페이지 개수
    # if right_index > paginator.num_pages:   # 오른쪽에 보여줄 페이지 개수가 전체 페이지 개수보다 크면전체 페이지 개수로 설정
    #     right_index = paginator.num_pages   
    # custom_range = range(left_index, right_index+1) # 페이지 범위 설정
    return page_obj