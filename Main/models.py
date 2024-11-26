from django.db import models
from Login.models import Profile
import re
from datetime import timedelta
from django.utils import timezone
# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="post_author")  # User who created the post
    caption = models.TextField()  # Caption with hashtags
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Post by {self.user.user.username} - {self.id}"

    def extract_hashtags(self):
        return re.findall(r'#\w+', self.caption)

    # Method to save hashtags associated with the post
    def save_hashtags(self):
        hashtags = self.extract_hashtags()
        for hashtag in hashtags:
            hashtag_obj, created = Hashtag.objects.get_or_create(name=hashtag)
            self.hashtags.add(hashtag_obj)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_hashtags()  # Automatically save hashtags when a post is saved
        
def upload_image(instance, filename):
    return "Posts/{instance.post.user.user.username}/{instance.post.id}_posts.png".format(instance=instance)


class Like(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='liked_post')
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='liker')
    liked_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"post --- {self.post.id} liked by {self.user.user.username}"
    

# Model to represent an Image associated with a Post
class Image(models.Model):
    post = models.ForeignKey(Posts, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image,blank=True)
    main_img=models.BooleanField(default=False)
    def __str__(self):
        return f"Image for Post {self.post.id}"


# Model for Hashtags
class Hashtag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    posts = models.ManyToManyField(Posts, related_name='hashtags', blank=True)

    def __str__(self):
        return self.name
    
    
class Comment(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='post_comment')
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='user_comment')
    text=models.CharField(max_length=255)
    comment_date=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural='Comment'
        db_table = 'Comment'
    
    def __str__(self):
        return self.text
    
    
def upload_image(instance, filename):
    return "story/{instance.user.user.username}/{instance.user.user.username}{instance.story_upload_date}{instance.id}.png".format(instance=instance)



    
class Story(models.Model):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='user_story')
    story_upload_date=models.DateTimeField(default=timezone.now)
    story=models.ImageField(upload_to=upload_image,blank=True)    
    expired=models.BooleanField(default=False)
    viewed_by=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='user_story_view',blank=True,null=True)
    class Meta:
        verbose_name_plural='Story'
        db_table = 'Story'
    
    def is_expired(self):
        # Check if 24 hours have passed since story creation
        if(timezone.now() - self.story_upload_date > timezone.timedelta(hours=24)):
            self.expired=True
            self.save()
            return True        
        return False    

    def __str__(self):
        return self.user.user.username +" Uploaded a story at "+str(self.story_upload_date)
