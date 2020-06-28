from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from app.models import Movies,Lists
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import TrigramSimilarity

import app.schema
import graphene

schema = graphene.Schema(query=app.schema.Query,mutation=app.schema.Mutation)


def index(request):
    return render(request,'index.html')


def listallmovies(request):
    page_number=request.GET.get('page')
    result = schema.execute(
		'''
		{
			allMovies(page:'''+str(page_number)+'''){
				page
				pages
				hasNext
				hasPrev
				nextPageNumber
				prevPageNumber
				objects{
				mid,
				title
				}
			}
		}
		'''
	)
    context={
		"movies":result.data["allMovies"][0]["objects"],
		"page" : result.data["allMovies"][0]["page"],
		"pages" : result.data["allMovies"][0]["pages"],
		"has_next" : result.data["allMovies"][0]["hasNext"],
		"has_prev" : result.data["allMovies"][0]["hasPrev"],
		"prev_page_number" : result.data["allMovies"][0]["prevPageNumber"],
		"next_page_number" : result.data["allMovies"][0]["nextPageNumber"]
	}
    print("============================")
    print(context)
    return render(request,"movies/page.html",context)


def singlemovie(request,id):
    movie = schema.execute(
		'''
		{
		  singleMovie(id:'''+str(id)+'''){
			mid
			voteCount
			voteAverage
			releaseDate
			language
			title
			adult
			popularity
			posterPath
			genreIds
			overview
		  }
		}
		'''
	)
    playlists = schema.execute(
		'''
		{
		  allLists{
			lid,
			name
		  }
		}
		'''
	)
    context = {'movie':movie.data['singleMovie'][0],'playlists':playlists.data['allLists']}
    return render(request,"movies/single_movie.html",context)


def singleplaylist(request,id):
    listx = schema.execute(
		'''
		{
			singleList(lid:'''+str(id)+'''){
				lid
				name
				mylist
			}
		}
		'''
	)
    context = { 'list' : listx.data['singleList'][0] , 'ply':listx.data['singleList'][0]['mylist']}
    return render(request,"watchlist/single_playlist.html",context)


def createmyownlist(request):
    listname = request.GET.get('listname')
    mid = request.GET.get('mid')
    result = schema.execute(
		'''
		mutation{
			createList(name:"'''+str(listname)+'''"){
	    	createListErrors
	    	lid
	  		}
		}
		'''
	)
    resultx = schema.execute(
		'''
		mutation{
			addToList(lid:'''+str(result.data['createList']['lid'])+''',mid:'''+str(mid)+'''){
				addToListErrors
			}
		}
		'''
    )
    return HttpResponseRedirect("singlemovie/"+str(mid))


def addtowatchlist(request):
    if (request.GET.get('mid')):
        mid = int(request.GET.get('mid'))
        lid = int(request.GET.get('lid'))
        result = schema.execute(
            '''
            mutation{
                addToList(lid:'''+str(lid)+''',mid:'''+str(mid)+'''){
                addToListErrors
                }
            }
            '''
        )
        return HttpResponseRedirect("singlemovie/"+str(mid))
    else:
        return render(request,"index.html")


def listalllist(request):
    playlists = schema.execute(
    '''
        {
          allLists{
            lid,
            name
          }
        }
    '''
    )
    context = {'playlists':playlists.data['allLists']}
    return render(request,"watchlist/playlists.html",context)


def searchmovie(request):
    name=request.GET.get('name')

    if(name!=None):
        # res=Movies.objects.annotate(
        # 	search=SearchVector('title'),
        # ).filter(search=name)
        res=Movies.objects.annotate(
        similarity=TrigramSimilarity('title', name),
        ).filter(similarity__gt=0.01).order_by('-similarity')
        print(res)
        if(res):
            context={
                "name" : name,
                "hasMovies" : True,
                "movies" :	res
            }
            print(context)
            return render(request,"movies/search_movie.html",context)
    context={
        "hasMovies" : False
    }
    return render(request,"movies/search_movie.html",context)


def recommendmovies(request):
    lid=request.GET.get('lid')
    context = {
        
    }
    return render(request,"watchlist/recommend_movies.html",context)


