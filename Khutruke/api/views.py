from django.shortcuts import render
from rest_framework import generics
from khutrukeapp.models import Item
from khutrukeapp.serializers import ItemSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class ItemListAPIView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
@csrf_exempt
def delete_item(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item does not exist'}, status=404)
    
    if request.method == 'DELETE':
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Only DELETE method is allowed'}, status=405)