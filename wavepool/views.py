from django.template import loader
from django.http import HttpResponse

from wavepool.models import NewsPost, UserStory


def front_page(request):
    template = loader.get_template('wavepool/frontpage.html')
    cover_story = NewsPost.objects.get(is_cover_story=True)
    newsposts = NewsPost.objects.all()
    context = {
        'cover_story': cover_story,
        'top_stories': newsposts[0:3],
        'archive': newsposts,
    }

    return HttpResponse(template.render(context, request))


def article(request):
    template = loader.get_template('wavepool/article.html')
    article = NewsPost.objects.get(pk=1)
    context = {
        'article': article
    }

    return HttpResponse(template.render(context, request))


def instructions(request):
    template = loader.get_template('wavepool/instructions.html')
    user_stories = UserStory.objects.all()
    context = {
        'user_stories': user_stories
    }
    return HttpResponse(template.render(context, request))
