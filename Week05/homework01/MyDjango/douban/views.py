from django.shortcuts import render
from .models import Comments


# Create your views here.
def index(request):
    search = request.GET.get('q')
    if not search:
        search = '金刚川'
    comments = Comments.objects.filter(movie_name=search).filter(stars__gt=3).order_by('stars').reverse()
    movie_name = Comments.objects.filter(movie_name=search).values('movie_name').first()
    if not movie_name:
        movie_name = ''
    else:
        movie_name = search
    return render(request, 'index.html', locals())
