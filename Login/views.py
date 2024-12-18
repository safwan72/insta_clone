from django.shortcuts import render, HttpResponseRedirect, HttpResponse,get_object_or_404
from django.urls import reverse, reverse_lazy
from . import forms,models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from Main.models import Posts,Image
from .models import Profile,Followers
from django.db.models import Q,Count
from Main.forms import CommentForm
# Create your views here.

def login_index(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Main:home'))
            messages.success(request, 'Logged in Successfully')
        else:
            messages.warning(request, 'Log In Failed. Check Proper Inputs')
            return HttpResponseRedirect(reverse('App_Login:login'))    
    return render(request, "Login/Login.html",context={'form': form,'username_class': 'form-control',})


def sign_index(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save()
            # user.email=form.cleaned_data.get('email')
            # user.username=form.cleaned_data.get('username')
            # user.password=form.cleaned_data.get('password1')
            user.save()
            messages.success(request, 'Account Created Successfully')
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request, "Login/Signup.html",context={'form': form,'username_class': 'form-control',})
from django.utils import timezone

@login_required
def myprofile(request,id):
# Get the current time zone
    form1 = CommentForm(request.POST) if request.method == 'POST' else CommentForm()
    user_profile = Profile.objects.get(user_id=id)
    my_user_id=Profile.objects.get(user__id=request.user.id)
            # Get the count of posts for this user
    my_profile=True if user_profile.user==request.user else False
    post_count = Posts.objects.filter(user=user_profile).count()
            
            # Get the count of followers for this user
    followers_count = Followers.objects.filter(me=user_profile).first()
    if followers_count:
        followers_count = followers_count.myfollowers.count()
    else:
        followers_count = 0
        
    if request.method == 'POST' and 'comment' in request.POST:
        if form1.is_valid():
            post_id = request.POST.get('post_id')
            post=get_object_or_404(Posts,id=post_id)
            comment=form1.save(commit=False)
            user_profile = Profile.objects.get(user_id=request.user.id)
            comment.user=user_profile
            comment.post=post
            comment.save()
            url = reverse('App_Login:profile', kwargs={'id': post.user.user.id})
            return HttpResponseRedirect(url)
            # Get the count of following for this user
    following_count = Followers.objects.filter(myfollowers=user_profile).count()
    # already_followed=Followers.objects.get(me=my_user_id).myfollowers.all().filter(user_id=user_profile.id)
    already_followed = Followers.objects.filter(myfollowers=my_user_id)
    already_following=False
# Check if the `myfollowers` Many-to-Many field contains `user_profile`
    if already_followed:
            for follower in already_followed:  
                if user_profile==follower.me:
                    already_following=True  # The user is a follower
# The user is not a follower
    # Fetch all posts by the user
    posts = Posts.objects.filter(user=user_profile).select_related('user').prefetch_related('images', 'hashtags','post_comment').annotate(
                like_count=Count('liked_post'),
                comment_count=Count('post_comment')
            )
        # Fetch the featured image for each post (main_img=True)
    for post in posts:
        post.featured_image = post.images.filter(main_img=True).first()
    context = {
                'profile': user_profile,
                'post_count': post_count,
                'followers_count': followers_count,
                'following_count': following_count,
                'posts':posts,
                'my_profile':my_profile,
                'already_followed':already_following,
                'form1':form1,
            }
    return render(request, "Profile/Profile.html",context=context)


@login_required
def logout_user(request):
    print("logout")
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))





@login_required
def follow(request,id):
    user_profile = Profile.objects.get(user_id=id)
    my_user_id=Profile.objects.get(user__id=request.user.id)
    already_followed=models.Followers.objects.filter(me=user_profile)
    print(already_followed)
    if  already_followed:
        for followers in already_followed:
            followers.myfollowers.add(my_user_id)
            followers.save()
    return HttpResponseRedirect(reverse('App_Main:home'))
   
   
@login_required
def unfollow(request,id):
    following_user=Profile.objects.get(user_id=id)
    print(following_user)
    follower_user=Profile.objects.get(user__id=request.user.id)
    print(follower_user)
    already_followed=models.Followers.objects.filter(me=following_user,myfollowers=follower_user)
    if already_followed.exists():
        for followers in already_followed:
            if following_user==followers.me:
            #     print(following_user.my_followers)
                followers.myfollowers.remove(follower_user)
    return HttpResponseRedirect(reverse('App_Main:home'))




@login_required
def edit_profile(request,id):
    user_profile = Profile.objects.get(user_id=id)
    print(user_profile)
    form=forms.EditProfile(instance=user_profile)
    if request.method=='POST':
        form=forms.EditProfile(request.POST,request.FILES,instance=user_profile)
        form.save(commit=True)
        form=forms.EditProfile(instance=user_profile)
        return HttpResponseRedirect(reverse(f"App_Login:profile",kwargs={'id': id}))
    return render(request, "Profile/EditProfile.html",context={'form':form})
