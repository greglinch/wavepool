from django.template import loader
from django.http import HttpResponse

from wavepool.models import NewsPost


def front_page(request):
    template = loader.get_template('wavepool/frontpage.html')
    newsposts = NewsPost.objects.all()
    context = {
        'cover_story': newsposts[0],
        'top_stories': newsposts[1:4],
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
