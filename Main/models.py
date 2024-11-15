from django.db import models
from Login.models import Profile
import re
# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)  # User who created the post
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




# Model to represent an Image associated with a Post
class Image(models.Model):
    post = models.ForeignKey(Posts, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image,blank=True)
    
    def __str__(self):
        return f"Image for Post {self.post.id}"


# Model for Hashtags
class Hashtag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    posts = models.ManyToManyField(Posts, related_name='hashtags', blank=True)

    def __str__(self):
        return self.name