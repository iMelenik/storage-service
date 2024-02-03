from rest_framework.generics import CreateAPIView, ListAPIView

from upload.models.file import File
from upload.serializers import FileSerializer


class UploadFileView(CreateAPIView):
    """
    Creates File object and saves it to the database. Starts processing of the file in the background.
    """
    serializer_class = FileSerializer


class FilesListView(ListAPIView):
    """
    Returns a list of all files with their data and status processing
    """
    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.all()
