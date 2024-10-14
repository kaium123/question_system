# questions/views.py

from .models import Tag, Question, FavoriteQuestion, ReadQuestion
from .serializers import TagSerializer, QuestionSerializer, FavoriteQuestionSerializer, ReadQuestionSerializer
from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.db import connection 
from django.db.models import Prefetch
from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tag
from .serializers import TagSerializer
from .managers import TagManager  # Assuming TagManager is in a separate file, adjust the import as needed
from .models import get_tag_question_statistics  # If it's inside models


class TagWithCountView(APIView):

    def get(self, request):
        origin = request.GET.get('origin')
        tag_id = request.GET.get('tag_id')

        try:
            # Use manager methods for tag queries
            if origin != "child":
                if tag_id:
                    Tag.objects
                    query_data = Tag.objects.filter(id=tag_id).prefetch_related('question_set')
                else:
                    query_data = Tag.objects.get_root_tags().prefetch_related('question_set')
            else:
                if tag_id:
                    query_data = Tag.objects.filter(parent_id=tag_id).prefetch_related('question_set')

            print("SQL Query:", query_data.query)

            # Collect statistics for each tag
            tag_statistics = []
            for tag in query_data:
                tag_name = tag.tag_name
                res = Tag.objects.get_tag_question_statistics(tag.id)  # Use manager method to get statistics
                tag_statistics.append({
                    'tag_id': tag.id,
                    'name': tag_name,
                    'statistics': res,
                })
                print(f"Tag ID: {tag.id}, Name: {tag_name}, Statistics: {res}")

            return Response(tag_statistics, status=status.HTTP_200_OK)

        except Tag.DoesNotExist:
            return Response({
                'data': {},
                'message': 'Tag not found.'
            }, status=status.HTTP_404_NOT_FOUND)


class TagCreateView(APIView):

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            tag = serializer.save()
            return Response({
                'data': TagSerializer(tag).data,
                'message': 'Tag created successfully.'
            }, status=status.HTTP_201_CREATED)

        return Response({
            'data': serializer.errors,
            'message': 'Validation failed.'
        }, status=status.HTTP_400_BAD_REQUEST)

            

class TagListView(APIView):
    
    def get(self, request):
        parent_id = request.GET.get('parent_id')
        
        try:
            if parent_id is not None:
                query_data = Tag.objects.filter(parent__id=parent_id).prefetch_related('question_set')
            else:
                query_data = Tag.objects.filter(parent__isnull=True).prefetch_related('question_set')
                
            print("SQL Query:", query_data.query)

            if not query_data.exists():
                return Response({'message': 'No tags found for the given parent_id.'}, status=status.HTTP_404_NOT_FOUND)

            serialized_tags = []
            for tag in query_data:
                serialized_tags.append({
                    'id': tag.id,
                    'name': tag.tag_name,
                    'parent_id': tag.parent.id if tag.parent else None,
                    'step': tag.step,
                })

            return Response(serialized_tags, status=status.HTTP_200_OK)


        except Tag.DoesNotExist:
            return Response({
                'data': {},
                'message': 'Tag not found.'
            }, status=status.HTTP_404_NOT_FOUND)
            
            
class QuestionPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'limit'  
    max_page_size = 100

class QuestionListView(APIView):
    pagination_class = QuestionPagination

    def get(self, request):
        tag_id = request.GET.get('tag_id')
        filter_type = request.GET.get('filter')

        queryset = Question.objects.filter(tag_id=tag_id)
        
        if filter_type == '!read':
            read_question_ids = ReadQuestion.objects.values_list('question_id', flat=True)
            queryset = queryset.exclude(id__in=read_question_ids)
        elif filter_type == 'read':
            read_question_ids = ReadQuestion.objects.values_list('question_id', flat=True)
            queryset = queryset.filter(id__in=read_question_ids)
            
        print("SQL Query:", queryset.query)    
        
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
    
        serializer = QuestionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class QuestionView(APIView):
    serializer_class = QuestionSerializer
    
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            tag = serializer.save()
            return Response({
                'data': QuestionSerializer(tag).data,
                'message': 'Question created successfully.'
            }, status=status.HTTP_201_CREATED)

        return Response({
            'data': serializer.errors,
            'message': 'Validation failed.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
class FavoriteQuestionView(APIView):

    def post(self, request):
        serializer = FavoriteQuestionSerializer(data=request.data)
        if serializer.is_valid():
            favorite_question = serializer.save()
            return Response({
                'data': FavoriteQuestionSerializer(favorite_question).data,
                'message': 'Favorite question added successfully.'
            }, status=status.HTTP_201_CREATED)

        return Response({
            'data': serializer.errors,
            'message': 'Validation failed.'
        }, status=status.HTTP_400_BAD_REQUEST)


class ReadQuestionView(APIView):

    def post(self, request):
        serializer = ReadQuestionSerializer(data=request.data)
        if serializer.is_valid():
            read_question = serializer.save()
            return Response({
                'data': ReadQuestionSerializer(read_question).data,
                'message': 'Read question added successfully.'
            }, status=status.HTTP_201_CREATED)

        return Response({
            'data': serializer.errors,
            'message': 'Validation failed.'
        }, status=status.HTTP_400_BAD_REQUEST)