from datetime import datetime
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import json
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import jplaceapp.models




def home(request):
    title = "Welcome to Jplace"
    testimonies_list = Testimonies.objects.all().order_by('-id')  # [:2]
    paginator = Paginator(testimonies_list, 1)
    page = request.GET.get('page')
    try:
        testimonies = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer, deliver first page
        testimonies = paginator.page(1)
    except EmptyPage:
        #if page is out of range, deliver last page of result
        testimonies = paginator.page(paginator.num_pages)

    context = {
        "title": title,
        "testimonies": testimonies,

    }
    return render(request, "home.html", context)


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    testimony_list = user.testimonies_set.order_by('-id')
    paginator = Paginator(testimony_list, 1)
    page = request.GET.get('page')
    try:
        testimony = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        testimony = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page of result
        testimony = paginator.page(paginator.num_pages)
    context = {
        'testimony': testimony,
        'username': username,
        'show_tags': True,
    }
    return render(request, 'user_page.html', context)


'''
def user_page(request, username):
    user = get_object_or_404(User, username=username)
    testimony = user.testimonies_set.order_by('-id')
    paginator = Paginator(testimony, ITEMS_PER_PAGE)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    try:
        testimony = paginator.get_page(page - 1)
    except:
        raise Http404

    # is_friend = Friendship.objects.filter(from_friend=request.user,to_friend=user )

    context = {
        'testimony': testimony,
        'username': username,
        'show_tags': True,
        'show_edit': username == request.user.username,
        'show_paginator': paginator.pages > 1,
        'has_prev': paginator.has_previous_page(page - 1),
        'has_next': paginator.has_next_page(page - 1),
        'page': page,
        'pages': paginator.pages,
        'next_page': page + 1,
        'prev_page': page - 1
    }
    return render(request, 'user_page.html', context)

'''


def detail(request, testimonies_id):
    testimonies = get_object_or_404(Testimonies, pk=testimonies_id)
    liked = False
    if request.session.get('has_liked_' + str(testimonies_id), liked):
        liked = True
        print("liked {}_{}".format(liked, testimonies_id))
    context = {
        'testimonies': testimonies,
        'liked': liked
    }
    return render(request, 'detail.html', context)

'''
def like_count_testimonies(request):
    liked = False
    if request.method == 'GET':
        testimonies_id = request.GET.get['testimonies_id', '']
        testimonies = Testimonies.objects.get(id=int(testimonies_id))
        if request.session.get('has_liked_' + testimonies_id, liked):
            print("unlike")
            if testimonies.likes > 0:
                likes = testimonies.likes - 1
                try:
                    del request.session['has_liked_' + testimonies_id]
                except KeyError:
                    print("keyerror")
        else:
            print("like")
            request.session['has_liked_' + testimonies_id] = True
            likes = testimonies.likes + 1
    testimonies.likes = likes
    testimonies.save()
    return HttpResponse(likes, liked)
'''

def post(request, username):
    follow = request.POST['follow']
    user = User.objects.get(username=request.user.username)
    user_profile = User.objects.get(username=username)
    user_follower, status = UserFollowers.objects.get_or_create(user=user_profile)
    if follow == 'true':
        # follow user
        user_follower.followers.add(user)
    else:
        # unfollow user
        user_follower.followers.remove(user)
    return HttpResponse(json.dumps(""), content_type="application/json")

'''
@login_required(login_url='/')
def testimony_vote_page(request):
    if request.GET.has_key('id'):
        try:
            id = request.GET['id']
            shared_testimonies = VoteTestimonies.objects.get(id=id)
            user_voted = shared_testimonies.users_voted.filter(username=request.user.username)
            if not user_voted:
                shared_testimonies.votes += 1
                shared_testimonies.users_voted.add(request.user)
                shared_testimonies.save()
        except ObjectDoesNotExist:
            raise Http404('Testimony not found.')
    if request.META.has_key('HTTP_REFERER'):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect('/')
'''
def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    testimony = tag.testimony.order_by('-id')
    context = {
        'testimony': testimony,
        'tag_name': tag_name,
        'show_tags': True,
        'show_user': True,
    }
    return render(request, 'tag_page.html', context)


def tag_cloud_page(request):
    MAX_WEIGHT = 5
    tags = Tag.objects.order_by('name')
    # Calculate tag, min and max counts.
    min_count = max_count = tags[0].testimony.count()
    for tag in tags:
        tag.count = tag.testimony.count()
        if tag.count < min_count:
            min_count = tag.count
            if max_count < tag.count:
                max_count = tag.count
                # Calculate count range. Avoid dividing by zero.
    range = float(max_count - min_count)
    if range == 0.0:
        range = 1.0
        # Calculate tag weights.
    for tag in tags:
        tag.weight = int(
            MAX_WEIGHT * (tag.count - min_count) / range)
    context = {
        'tags': tags
    }
    return render(request, 'tag_cloud_page.html', context)


'''

def _testimonies_save(request, form):
    testimony, dummy = MyTestimony.objects.get_or_create(
        testimony=form.cleaned_data['testimony']
    )
    # Create or get bookmark.
    testimonies, created = Testimonies.objects.get_or_create(
        user=request.user,
        testimonies=testimony,
    )
    # Update bookmark title.
    testimonies.title = form.cleaned_data['title']
    # If the bookmark is being updated, clear old tag list.
    if not created:
        testimonies.tag_set.clear()
    # Create new tag list.
    tag_names = form.cleaned_data['tags'].split()
    for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        testimonies.tag_set.add(tag)

     # Share on the main page if requested.
    if form.cleaned_data['share']:
        shared_testimony, created = VoteTestimonies.objects.get_or_create(testimony=testimony)
        if created:
            shared_testimony.users_voted.add(request.user)
            shared_testimony.save()
    # Save bookmark to database.
    testimonies.save()
    return testimonies

'''


def _testimonies_save(request, form):
    testimony, dummy = MyTestimony.objects.get_or_create(
        testimony=form.cleaned_data['testimony']
    )
    # Create or get testimony.
    testimonies, created = Testimonies.objects.get_or_create(
        user=request.user,
        testimonies=testimony,
    )
    # Update testimony title.
    testimonies.title = form.cleaned_data['title']
    # If the testimony is being updated, clear old tag list.
    if not created:
        testimonies.tag_set.clear()
    # Create new tag list.
    tag_names = form.cleaned_data['tags'].split()
    for tag_name in tag_names:
        tag, dummy = Tag.objects.get_or_create(name=tag_name)
        testimonies.tag_set.add(tag)

        # Share on the main page if requested.
        # if form.cleaned_data['share']:
        # shared_testimony, created = VoteTestimonies.objects.get_or_create(testimony=testimony)
        # if created:
        #   shared_testimony.users_voted.add(request.user)
        # shared_testimony.save()
    # Save bookmark to database.
    testimonies.save()
    return testimonies




@csrf_exempt
@login_required(login_url='/')
def testimonies_save_page(request):
    if request.method == 'POST':
        form = TestimonySaveForm(request.POST, request.FILES)
        if form.is_valid():
            testimonies = _testimonies_save(request, form)
            return HttpResponseRedirect('/user/%s/' % request.user.username)
    elif request.GET.has_key('url'):
        url = request.GET['url']
        title = ''
        tags = ''
        try:
            my_testimony = MyTestimony.objects.get(url=url)
            testimonies = Testimonies.objects.get(
                my_testimony=my_testimony,
                user=request.user
            )
            title = Testimonies.title
            tags = ' '.join(
                tag.name for tag in Testimonies.tag_set.all()
            )
        except:
            pass
        form = TestimonySaveForm({
            'url': url,
            'title': title,
            'tags': tags
        })
    else:
        form = TestimonySaveForm()
    context = {
        'form': form
    }
    return render(request, 'testimonies_save.html', context)


'''
@csrf_exempt
@login_required(login_url='/')
def testimonies_save_page(request):
    if request.method == 'POST':
        form = TestimonySaveForm(request.POST)
        if form.is_valid():
            testimony, dummy = MyTestimony.objects.get_or_create(
                testimony=form.cleaned_data['testimony']
            )
            # Create or get bookmark.
            testimonies, created = Testimonies.objects.get_or_create(
                user=request.user,
                testimonies=testimony,
            )
            # Update bookmark title.
            testimonies.title = form.cleaned_data['title']
            # If the bookmark is being updated, clear old tag list.
            if not created:
                testimonies.tag_set.clear()
             # Create new tag list.
            tag_names = form.cleaned_data['tags'].split()
            for tag_name in tag_names:
                tag, dummy = Tag.objects.get_or_create(name=tag_name)
                testimonies.tag_set.add(tag)
                # Save bookmark to database.
            testimonies.save()
            return HttpResponseRedirect('/user/%s/' % request.user.username)
    else:
        form =TestimonySaveForm()
    variables = RequestContext(request, {
            'form': form
        })
    return render_to_response('testimonies_save.html', variables)
'''


def search_page(request):
    form = SearchForm()
    testimony = []
    show_results = False
    if request.GET.has_key('query'):
        show_results = True
        query = request.GET['query'].strip()
        if query:
            keywords = query.split()
            q = Q()
            for keyword in keywords:
                q &= Q(title__icontains=keyword)
                form = SearchForm({'query': query})
                testimony = Testimonies.objects.filter(q)[:10]
    context = {
        'form': form,
        'testimony': testimony,
        'show_results': show_results,
        'show_tags': True,
        'show_user': True,
    }

    if request.GET.has_key('ajax'):
        return render(request, 'testimony_list.html', context)
    else:
        return render(request, 'search.html', context)


def popular_page(request):
    today = datetime.today()
    yesterday = today - timedelta(1)
    shared_testimonies = VoteTestimonies.objects.filter(date__gt=yesterday)
    shared_testimonies = shared_testimonies.order_by('-votes')[:10]
    context = {
        'shared_testimonies': shared_testimonies
    }
    return render(request, 'popular_page.html', context)
