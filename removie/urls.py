from django.urls import path
from django.conf.urls import url
from django.contrib import admin

from django.views.decorators.csrf import csrf_exempt
from app import views
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('addtowatchlist',views.addtowatchlist),
    path('listallmovies', views.listallmovies),
    path('createmyownlist',views.createmyownlist),
    path('singlemovie/<int:id>', views.singlemovie),
    path('singleplaylist/<int:id>', views.singleplaylist),
    path('listalllist',views.listalllist),
    path('searchmovie',views.searchmovie),
    path('recommendmovies',views.recommendmovies),
    url('', views.index),
]
