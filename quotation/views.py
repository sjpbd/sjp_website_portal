from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Quote  # Assuming you have a Quote model
from rest_framework.response import Response
import random
from rest_framework import generics
from .serializers import QuoteSerializer

def daily_inspiration(request):
    return render(request, 'quotation/daily-inspiration.html')

@api_view(['GET'])
def random_quote(request):
    # Example of fetching a random quote from your model
    quotes = Quote.objects.all()
    if quotes.exists():
        quote = random.choice(quotes)
        return Response({
            'status': 'success',
            'text': quote.text,
            'author': quote.author,
            'source': quote.source,
        })
    else:
        return Response({'status': 'error', 'message': 'No quotes available.'})


class QuoteListView(generics.ListAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


