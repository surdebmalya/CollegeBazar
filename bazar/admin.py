from django.contrib import admin
from .models import USERS, ITEMS, USER_WISHLISTS, MESSAGES, CHATROOMS

# Register your models here.
admin.site.register(USERS)
admin.site.register(ITEMS)
admin.site.register(USER_WISHLISTS)
admin.site.register(CHATROOMS)
admin.site.register(MESSAGES)
