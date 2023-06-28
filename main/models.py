import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from uuid import uuid4
from datetime import datetime


# Create your models here.
def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['post/', ymd_path, uuid_name])

def get_file_path_somd(instance, filename):
    uuid_name = uuid4().hex
    return '/'.join(['somd/', uuid_name])


class Tag(models.Model): #태그
    name = models.CharField(max_length=30,null=False,blank=False)

class JoinRequest(models.Model): #가입신청서
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, default="")

    title =  models.CharField(max_length=50,blank=False,null=False)
    motivation = models.TextField()
    pub_date = models.DateTimeField()


class SOMD(models.Model):
    name = models.CharField(max_length=30)

    #소모임 소개
    intro = models.CharField(max_length=50, blank=True)
    #관리자
    admin = models.ForeignKey(User, related_name="somd_admin", on_delete=models.CASCADE, blank=False, null=False, default=1)

    #이미지관련
    profileimage = models.ImageField(upload_to=get_file_path_somd, blank=True, null=True, default='somd/somdDefaultImage.png')
    filename_prof = models.CharField(max_length=64, null=True)
    backgroundimage = models.ImageField(upload_to=get_file_path_somd, blank=True, null=True, default='somd/somdbackDefaultImage.png')
    filename_back = models.CharField(max_length=64, null=True)
    

    #대학/학과
    college = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    
    #태그
    tags = models.ManyToManyField(Tag, related_name='somds', blank=True)
    snslink = models.CharField(max_length=200, blank=True,null=True)
    
    #없앨듯..?
    # category = models.CharField(max_length=50, blank=True, null=True)

    #솜디 정회원
    join_members = models.ManyToManyField(User, related_name="join_members", blank=True)
    bookmark = models.ManyToManyField(User, related_name='bookmark', blank=True)

    #솜디 가입 대기회원
    waitTojoin_members = models.ManyToManyField(User, related_name="waitTojoin_members", blank=True)
    join_requests = models.ManyToManyField(JoinRequest, related_name="join_requests", blank=True)

    def __str__(self):
        return self.name
    
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    somds = models.ManyToManyField(SOMD, related_name="members", blank=True) #가입된 솜디

    rejected_somds = models.ManyToManyField(SOMD, related_name="rejected_somds", blank=True) #가입 거절된 솜디
    waiting_somds = models.ManyToManyField(SOMD, related_name="waiting_somds", blank=True) #가입 대기중솜디




class Post(models.Model):
    somd = models.ForeignKey(SOMD, null=False, blank=False, on_delete=models.CASCADE,related_name='posts')

    title = models.CharField(max_length=200,null=False,blank=False)
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    content = models.TextField()

    like = models.ManyToManyField(User, related_name='like', blank=True)
    like_count = models.IntegerField(default=0)
    
    comment_count = models.IntegerField(default=0)

    scrap = models.ManyToManyField(User, related_name='scrap', blank=True)
    
    is_fixed = models.BooleanField(default=False)

    is_secret = models.BooleanField(default=False)


    def __str__(self):
        return self.title
    
    def summary(self):
        if len(self.content) > 65:
            return self.content[:65]+'...'
        else:
            return self.content
        

    class Meta:
        ordering = ['-pub_date']

class Comment(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField()
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title+" : "+self.content[:20]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # self.post.update_num_comments()

class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    filename = models.CharField(max_length=64, null=True)
    
    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(Images, self).delete(*args, **kargs)


class Alram(models.Model):
    somd = models.ForeignKey(SOMD, null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    sendUser = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    
    date = models.DateTimeField(null=True, blank=True)

    type = models.TextField(blank=False)

class UserAlram(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alrams = models.ManyToManyField(Alram, related_name="alram", blank=True)
    new = models.BooleanField(default=False)