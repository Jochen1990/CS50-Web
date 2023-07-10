from django.contrib import admin
from .models import User, Category, Watchlist, Comments, Bids, Listings

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Watchlist)

