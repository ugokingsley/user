from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'jplace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #browsing
    url(r'^$', 'jplaceapp.views.index', name='index'),
    url(r'^all/$', 'jplaceapp.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^save/$', 'jplaceapp.views.testimonies_save_page', name='testimonies_save_page'),
    url(r'^tag/$', 'jplaceapp.views.tag_cloud_page', name='tag_cloud_page'),
    url(r'^search/$','jplaceapp.views.search_page', name='search_page'),
    url(r'^popular/$', 'jplaceapp.views.popular_page', name='popular_page'),
    #url(r'^like-testimonies/$', 'jplaceapp.views.like_count_testimonies', name='like_count_testimonies'),
    url(r'^likes/', include('likes.urls')),

    #user
    url(r'^user/(\w+)/$', 'jplaceapp.views.user_page', name='user_page'),
    url(r'^tag/([^\s]+)/$','jplaceapp.views.tag_page', name='tag_page'),
    #url(r'^vote/$', 'jplaceapp.views.testimony_vote_page', name='testimony_vote_page'),
    url(r'^testimony/(?P<testimonies_id>[0-9]+)/$','jplaceapp.views.detail',name='detail'),
    #user following
    url(r'^friendship/', include('friendship.urls')),
    #user registration
    url(r'^accounts/', include('registration.backends.default.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)