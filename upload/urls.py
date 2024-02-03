from django.urls import path

from upload.views import UploadFileView, FilesListView

app_name = 'upload'
urlpatterns = [
    path('upload', UploadFileView.as_view(), name='upload_file'),
    path('files', FilesListView.as_view(), name='files_list'),
]
