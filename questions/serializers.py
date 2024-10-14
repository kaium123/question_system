# questions/serializers.py

from rest_framework import serializers
from .models import Tag, Question, FavoriteQuestion, ReadQuestion

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'option1', 'option2', 'option3', 'option4', 'answer', 'tag']  # Update fields

class FavoriteQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteQuestion
        fields = '__all__'

class ReadQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadQuestion
        fields = ['id', 'user', 'question']  # Make sure to include 'user'
