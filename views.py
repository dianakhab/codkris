from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Women
from rest_framework import generics
from .serializers import WomenSerializer

# Create your views here.
class WomenAPIView(APIView):
    def get(self, request):
        w = Women.objects.all()
        return Response({"posts": WomenSerializer(w, many=True).data})

    def post(self, request):
        serializer = WomenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        post_new = Women.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            cat_id=request.data['cat_id']
        )
        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)

        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)

        try:
            instance = Women.objects.get(pk=pk)
            instance.delete()
            return Response({"message": f"Post with id {pk} has been deleted"})
        except Women.DoesNotExist:
            return Response({"error": "Object does not exist"})

# class WomenAPIView(generics.ListAPIView):
#     queryset = Women.objects.all();
#     serializer_class = WomenSerializer;