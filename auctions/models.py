from django.contrib.auth.models import AbstractUser
from django.db import models

category = (
    ('Clothes' , 'Clothes'),
    ('Electronics' ,'Electronics' ),
    ('Groceries','Groceries'),
    ('Beauty','Beauty'),
    ('Books','Books'),
    ('Sports','Sports'),
    ('Pet supplies','Pet supplies'),
    ('Others','Others'),

)


class User(AbstractUser):
    pass

class Auctions(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=30,choices=category,default=None)
    image = models.ImageField(blank = True , default = 'default.jpg')

    def __str__(self):
        return self.title

class Biding(models.Model):
    bid = models.DecimalField(max_digits=5, decimal_places=2 , blank = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product =  models.ForeignKey(Auctions , on_delete = models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product.title) + ' ' + str(self.author.username)

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField(blank=True)
    comment_on = models.ForeignKey(Auctions, on_delete = models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username) + str(self.comment_on.title)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE )
    watchlist = models.ForeignKey(Auctions , on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username
    
