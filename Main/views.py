from django.shortcuts import render
from Login.models import Profile,Followers
from . import models
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home_index(request):
    posts=[]
    userProfile=Profile.objects.filter(user_id=2)
    if userProfile:
        userProfile = userProfile[0]
        user1 = userProfile.my_followers.all()
        if user1:
            for friend in user1:
                all_post = models.Posts.objects.filter(user=friend.me).all()
                if all_post:
                    for post in all_post:
                        posts.append(post)

        mypost = userProfile.post_author.all()
        if mypost:
            for post in mypost:
                posts.append(post)
            # print(posts)
            
    stories=[]
    userProfile=Profile.objects.filter(user_id=2)
    if userProfile:
        userProfile = userProfile[0]
        user1 = userProfile.my_followers.all()
        if user1:
            for friend in user1:
                all_stories = models.Story.objects.filter(user=friend.me).all()
                if all_stories:
                    for story in all_stories:
                        stories.append(story)

        # mypost = userProfile.post_author.all()
        # if mypost:
        #     for post in mypost:
        #         posts.append(post)
        print(stories)
    return render(request, "Home/Home.html",context={'posts':posts,'stories':stories})



