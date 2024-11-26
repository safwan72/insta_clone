from django import forms
from . import models



class ImageUploadForm(forms.ModelForm):
    class Meta:
        model=models.Story
        fields = ['story']
        

class PostForm(forms.ModelForm):
    caption=forms.CharField(required=False,widget=forms.Textarea(attrs={'col':8,"row":6,'placeholder':"Enter Your Caption Here",'class':'form-control'}))    

    class Meta:
        model=models.Posts
        fields = ('caption',)
        
class CommentForm(forms.ModelForm):
    text=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':"Enter Your Comment here",'class':'form-control'}))    

    class Meta:
        model=models.Comment
        fields = ('text',)

    # def __init__(self, *args, **kwargs):
    #     super(CommentForm, self).__init__(*args, **kwargs)
    #     # Change the widget to a TextInput (single-line input)
    #     self.fields['comment'].widget = forms.TextInput(attrs={
    #         'class': 'form-control',  # Optional: CSS class for styling
    #         'placeholder': 'Enter your comment here...',  # Placeholder text
    #     })