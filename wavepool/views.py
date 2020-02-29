from django.template import loader
from django.http import HttpResponse

from wavepool.models import NewsPost


# Create your views here.
def front_page(request):
    template = loader.get_template('wavepool/frontpage.html')
    newsposts = NewsPost.objects.all()
    context = {
        'cover_story': newsposts[0],
        'top_stories': newsposts[1:4],
        'archive': newsposts,
    }

    return HttpResponse(template.render(context, request))
