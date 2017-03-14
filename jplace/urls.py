from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from jplaceapp.models import Testimonies,MyTestimony

urlpatterns = [
    # Examples:
    # url(r'^$', 'jplace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #browsing
    url(r'^$', 'jplaceapp.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^save/$', 'jplaceapp.views.testimonies_save_page', name='testimonies_save_page'),
    url(r'^tag/$', 'jplaceapp.views.tag_cloud_page', name='tag_cloud_page'),
    url(r'^search/$','jplaceapp.views.search_page', name='search_page'),
    url(r'^popular/$', 'jplaceapp.views.popular_page', name='popular_page'),
    #user
    url(r'^user/(\w+)/$', 'jplaceapp.views.user_page', name='user_page'),
    url(r'^tag/([^\s]+)/$','jplaceapp.views.tag_page', name='tag_page'),
    url(r'^vote/$', 'jplaceapp.views.testimony_vote_page', name='testimony_vote_page'),
    url(r'^testimony/(?P<testimonies_id>[0-9]+)/$','jplaceapp.views.detail',name='detail'),
    #url(r'^comments/', include('django_comments.urls')),
    #user registration
    url(r'^accounts/', include('registration.backends.default.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)