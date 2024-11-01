from haystack import indexes
from .models import Profile

class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='first_name')

    def get_model(self):
        return Profile

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
        