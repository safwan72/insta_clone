from django import forms
from . import models



class ImageUploadForm(forms.ModelForm):
    class Meta:
        model=models.Story
        fields = ['story']
        
        
        
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