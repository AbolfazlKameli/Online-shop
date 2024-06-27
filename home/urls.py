from django.urls import path, include
from . import views

app_name = 'home'

bucket_urls = [
    path('', views.BucketHome.as_view(), name="bucket_home"),
    path('delete_object/<str:key>/', views.BucketHomeObjectDelete.as_view(), name="bucket_home_delete"),
    path('download_object/<str:key>/', views.BucketHomeObjectDownload.as_view(), name='bucket_home_download'),
    path('upload_object/', views.BucketHomeObjectUpload.as_view(), name='bucket_home_upload'),
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<str:category_slug>/', views.HomeView.as_view(), name='category_filter'),
    path('bucket/', include(bucket_urls)),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('comment/reply/<int:product_id>/<int:comment_id>/', views.CreatCommentReplyView.as_view(), name='comment_reply'),
    path('comment/delete/<int:comment_id>/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
