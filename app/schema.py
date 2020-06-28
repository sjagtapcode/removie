import graphene
from graphene_django import DjangoObjectType

from .models import Movies,Lists


class MovieType(DjangoObjectType):
    class Meta:
        model = Movies


class MovieTitleType(DjangoObjectType):
    class Meta:
        model = Movies
        fields = ('mid','title')


class ListType(DjangoObjectType):
    class Meta:
        model = Lists


class ListAndMovieType(graphene.ObjectType):
    lid = graphene.Int()
    name = graphene.String()
    mylist = graphene.List(MovieTitleType)


class MoviePaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    next_page_number = graphene.Int()
    prev_page_number = graphene.Int()
    objects = graphene.List(MovieTitleType)


class Query(graphene.ObjectType):
    all_movies = graphene.List(
        MoviePaginatedType,
        page=graphene.Int()
    )
    single_movie = graphene.List(
        MovieType,
        id=graphene.Int()
    )
    recommend_movies = graphene.List(
        MovieTitleType,
        lid=graphene.Int()
    )
    all_lists = graphene.List(ListType)
    single_list = graphene.List(
        ListType,
        lid=graphene.Int()
    )
    try_list = graphene.List(
        ListAndMovieType,
        lid=graphene.Int()
    )

    @staticmethod
    def resolve_try_list(self, info, lid):
        getlistbyid = Lists.objects.get( lid__exact = lid )
        print(getlistbyid)
        movielist = Movies.objects.filter(mid__in=getlistbyid.mylist)
        context= {ListAndMovieType(
            lid=lid,
            name=getlistbyid.name,
            mylist=movielist
        )
        }
        return context

    @staticmethod
    def resolve_single_list(self, info, lid):
        getlistbyid= Lists.objects.get(lid__exact=lid)
        return {getlistbyid}

    @staticmethod
    def resolve_recommend_movies(self, info, lid):
        getmovieids = Lists.objects.get(lid__exact=lid)[0].mylist
        getmovies = Movies.objects.filter(mid__in=getmovieids)
        return getmovies

    @staticmethod
    def resolve_single_movie(self, info, id):
        return {Movies.objects.get(mid=id)}

    @staticmethod
    def resolve_all_lists(self, args):
        return Lists.objects.all()

    @staticmethod
    def resolve_all_movies(self, info, page):
        page_size = 20
        if page == 0:
            page=1
        qs = Movies.objects.all()
        skip = page_size*(page-1)
        num_pages=qs.count()/page_size
        qs = qs[skip:skip+page_size]
        has_next=True
        has_previous = True
        if page == num_pages:
            has_next = False
        if page == 1:
            has_previous = False
        return {MoviePaginatedType(
            page = page,
            pages = num_pages,
            has_next = has_next,
            next_page_number = page+1,
            has_prev = has_previous,
            prev_page_number = page-1,
            objects = qs,
        )}


class CreateList(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    create_list_errors = graphene.String()
    lid=graphene.Int()

    @staticmethod
    def mutate(self, info, name):
        new_list = Lists.objects.create(name=name,mylist=list())
        return CreateList(create_list_errors="",lid=new_list.lid)


class AddToList(graphene.Mutation):
    class Arguments:
        lid = graphene.Int()
        mid = graphene.Int()

    add_to_list_errors = graphene.String()

    @staticmethod
    def mutate(self, info, lid, mid):
        getlist = Lists.objects.filter(lid__exact=lid)[0]
        listed = getlist.mylist
        listed.append(mid)
        reply = Lists.objects.filter(lid__exact=lid).update(mylist=listed)
        return AddToList(add_to_list_errors=reply)


class Mutation(graphene.ObjectType):
    create_list = CreateList.Field()
    add_to_list = AddToList.Field()


