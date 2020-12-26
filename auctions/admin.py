from django.contrib import admin
from .models import User , Auctions , Biding, Comments, Watchlist

# Register your models here.
admin.site.register(Auctions)
admin.site.register(Biding)
admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Watchlist)