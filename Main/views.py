from Login.models import Profile,Followers
from . import models,forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, HttpResponse,get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db.models import Q,Count

# Create your views here.
@login_required
def home_index(request):
    form = forms.ImageUploadForm(request.POST, request.FILES) if request.method == 'POST' else forms.ImageUploadForm()
    form1 = forms.CommentForm(request.POST) if request.method == 'POST' else forms.CommentForm()

    if request.method == 'POST' and 'story' in request.POST and form.is_valid():
            story=form.save(commit=False)
            user_profile = Profile.objects.get(user_id=request.user.id)
            story.user=user_profile
            story.save()
            return HttpResponseRedirect(reverse('App_Main:home'))
    elif request.method == 'POST' and 'comment' in request.POST:
        if form1.is_valid():
            post_id = request.POST.get('post_id')
            post=get_object_or_404(models.Posts,id=post_id)
            comment=form1.save(commit=False)
            user_profile = Profile.objects.get(user_id=request.user.id)
            comment.user=user_profile
            comment.post=post
            comment.save()
            return HttpResponseRedirect(reverse('App_Main:home'))
        else:
            print(form1.errors)
  
    posts=[]
    seen_ids = set() 
    userProfile = Profile.objects.filter(user_id=request.user.id).first()  # Use .first() to get the first profile or None

    if userProfile:
    # Get all users that the current user is following (i.e., 'my_followers')
        user1 = userProfile.my_followers.all()

    # Initialize an empty list to collect posts
        all_posts = []

    # Add posts from the user's own profile
        user_posts = models.Posts.objects.filter(
        Q(user=userProfile)
    ).prefetch_related('images', 'hashtags', 'post_comment', 'liked_post').annotate(
        like_count=Count('liked_post'),
        comment_count=Count('post_comment')
    )
        all_posts.extend(user_posts)  # Add posts from the user

    # If the user has followers, include their posts as well
        if user1:
            for friend in user1:
                print("Friend:", friend)
            # Add posts from each friend's profile
                friend_posts = models.Posts.objects.filter(
                Q(user=friend.me)  # Get posts from the friend
            ).prefetch_related('images', 'hashtags', 'post_comment', 'liked_post').annotate(
                like_count=Count('liked_post'),
                comment_count=Count('post_comment')
            )
                all_posts.extend(friend_posts)  # Add posts from the friend

    # Now 'all_posts' contains the posts from userProfile and their followers
    if all_posts:
        for post in all_posts:
            post.featured_image = post.images.filter(main_img=True).first()
            if post.id not in seen_ids:
                posts.append(post)  # Add post to the unique posts list
                seen_ids.add(post.id)  # Mark this post ID as seen
            
    stories=[]
    userProfile=Profile.objects.filter(user_id=request.user.id)
    if userProfile:
        userProfile = userProfile[0]
        my_stories = models.Story.objects.filter(user=userProfile).all()
        if my_stories:
            for story in my_stories:
                story.is_expired()
                if(story.expired==False):
                    # print(story,story.expired)
                    stories.append(story)
        user1 = userProfile.my_followers.all()
        if user1:
            for friend in user1:
                all_stories = models.Story.objects.filter(user=friend.me).all()
                if all_stories:
                    for story in all_stories:
                        story.is_expired()
                        if(story.expired==False):
                            # print(story,story.expired)
                            stories.append(story)
        # print(stories)                    
    return render(request, "Home/Home.html",context={'posts':posts,'stories':stories,'form':form,'form1':form1})



def explore_view(request):
    my_user_id=Profile.objects.get(user__id=request.user.id)
    users=Profile.objects.all().exclude(user__id=request.user.id)
    followers_of_this_profile = Followers.objects.filter(myfollowers=my_user_id)
    if users:
        for user in users:
            for follower in followers_of_this_profile:                
                if user ==follower.me:
                    user.is_following=True
                
    
    # for user_follower in already_followed.myfollowers.all():
        
    
    
    # Get all Followers objects where this profile is in 'myfollowers'

# # If you want to get the actual profiles that are following this profile:
#     profiles_following_this_profile = [follower.me for follower in followers_of_this_profile]
#     print("followers",profiles_following_this_profile)
    
    
#     following_instances = Followers.objects.filter(me=my_user_id)

# # Get the profiles being followed (from the `myfollowers` field)
#     profiles_being_followed = []
#     for instance in following_instances:
#         profiles_being_followed.extend(instance.myfollowers.all())
    
#     print("followings",profiles_being_followed)
    
#     if users:
#         for user in users:
#             if already_followed and user in already_followed.myfollowers.all():
#                 user.is_following=True
    return render(request, "Explore/Explore.html",context={"users":users})




