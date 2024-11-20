from Login.models import Profile,Followers
from . import models,forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.db.models import Q,Count
# Create your views here.
@login_required
def home_index(request):
    if request.method == 'POST':
        form = forms.ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            story=form.save(commit=False)
            user_profile = Profile.objects.get(user_id=2)# Save the uploaded image to the database
            story.user=user_profile
            story.save()
            return HttpResponseRedirect(reverse('App_Main:home'))
    else:
        form = forms.ImageUploadForm()    
    posts=[]
    userProfile=Profile.objects.filter(user_id=2)
    if userProfile:
        userProfile = userProfile[0]
        user1 = userProfile.my_followers.all()
        if user1:
            for friend in user1:
                all_post = models.Posts.objects.filter(
    Q(user=friend.me) | Q(user=userProfile)
).prefetch_related('images', 'hashtags', 'post_comment','liked_post').annotate(like_count=Count('liked_post'),comment_count=Count('post_comment'))
                if all_post:
                    for post in all_post:
                        post.featured_image = post.images.filter(main_img=True).first()
                        print(post.hashtags)
                        print(post.images)
                        posts.append(post)
            
    stories=[]
    userProfile=Profile.objects.filter(user_id=2)
    if userProfile:
        userProfile = userProfile[0]
        my_stories = models.Story.objects.filter(user=userProfile).all()
        if my_stories:
            for story in my_stories:
                stories.append(story)
        user1 = userProfile.my_followers.all()
        if user1:
            for friend in user1:
                all_stories = models.Story.objects.filter(user=friend.me).all()
                if all_stories:
                    for story in all_stories:
                        stories.append(story)
    return render(request, "Home/Home.html",context={'posts':posts,'stories':stories,'form':form})



