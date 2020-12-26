from .models import Auctions, Biding, Comments
from django.forms import ModelForm

class AuctionCreationForm(ModelForm):
    class Meta:
        model = Auctions
        fields = ['title' , 'description' , 'price', 'category' , 'image']

class BidingForm(ModelForm):
    class Meta:
        model = Biding
        fields = ['bid']

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']