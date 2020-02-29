from django.contrib import admin
from wavepool.models import NewsPost, UserStory, AcceptanceCriteria


class AcceptanceCriteriaAdmin(admin.StackedInline):
    model = AcceptanceCriteria


class UserStoryAdmin(admin.ModelAdmin):
    model = UserStory
    inlines = [AcceptanceCriteriaAdmin, ]

admin.site.register(NewsPost)
admin.site.register(UserStory, UserStoryAdmin)
