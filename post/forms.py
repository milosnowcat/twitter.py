from django import forms
from .models import Post, Offer, Topic

# This is a Django form class for creating an Offer object with fields for head, content, and image.
class OfferForm(forms.ModelForm):
    head = forms.CharField(
        widget=forms.TextInput(attrs={
            'maxlength':100,
            'placeholder':"Title"
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class':'form-control w-100',
            'id':'contentsBox', 'rows':'3',
            'placeholder':"Body"
        })
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'onchange':'previewFile()'
        })
    )

    # This class defines the model and fields for an Offer object in Python.
    class Meta:
        model = Offer
        fields = ['head', 'content', 'image']

# The `PostForm` class is a Django ModelForm that includes fields for `content` and `image`, with
# corresponding widgets and attributes.
class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class':'form-control w-100',
            'id':'contentsBox', 'rows':'3',
            'placeholder':"What's going on?"
        })
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'onchange':'previewFile()'
        })
    )

    # This class defines the model and fields for a Post object.
    class Meta:
        model = Post
        fields = ['content', 'image']

# This is a Django form class for creating or updating a Topic model instance with a single field for
# the name attribute, which is a CharField with optional input validation and a placeholder text.
class TopicForm(forms.ModelForm):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'maxlength':100,
            'placeholder':"topic1 topic2"
        })
    )

    # This class defines the model and fields for a Topic in Python.
    class Meta:
        model = Topic
        fields = ['name']
