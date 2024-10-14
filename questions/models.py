from django.db import models
from django.contrib.auth.models import User

class TagManager(models.Manager):
    def get_root_tags(self):
        return self.filter(parent__isnull=True)
    
    def get_tag_question_statistics(self, root_tag_id):
        print("tag_id. ---  ", root_tag_id)
        query = """
            WITH RECURSIVE TagHierarchy AS (
                SELECT t.id AS tag_id
                FROM questions_tag t
                WHERE t.id = %s

                UNION ALL

                SELECT t.id AS tag_id
                FROM questions_tag t
                INNER JOIN TagHierarchy th ON t.parent_id = th.tag_id
            )
            SELECT
                SUM(COUNT(DISTINCT q.id)) OVER() AS total_questions,
                SUM(COUNT(DISTINCT rq.id)) OVER() AS total_read_questions,
                SUM(COUNT(DISTINCT fq.id)) OVER() AS total_favorite_questions
            FROM TagHierarchy th
            LEFT JOIN questions_question q ON q.tag_id = th.tag_id
            LEFT JOIN questions_readquestion rq ON rq.question_id = q.id
            LEFT JOIN questions_favoritequestion fq ON fq.question_id = q.id
            GROUP BY th.tag_id;
        """
        
        print("Executing SQL Query:", query % root_tag_id)  

        with connection.cursor() as cursor:
            cursor.execute(query, [root_tag_id])
            result = cursor.fetchone()  

        return {
            'total_questions': result[0],
            'total_read_questions': result[1],
            'total_favorite_questions': result[2],
        }


# Tag model using the custom manager
class Tag(models.Model):
    tag_name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    step = models.IntegerField(default=0)

    objects = TagManager()  # Assign the custom manager

    def __str__(self):
        return self.tag_name


class QuestionManager(models.Manager):
    def with_answer(self, answer):
        return self.filter(answer=answer)

    def by_tag(self, tag_id):
        return self.filter(tag__id=tag_id)


class Question(models.Model):
    question = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    objects = QuestionManager() 

    def __str__(self):
        return self.question


class FavoriteQuestionManager(models.Manager):
    def for_user(self, user):
        return self.filter(user=user)

    def by_question(self, question_id):
        return self.filter(question__id=question_id)


class FavoriteQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = FavoriteQuestionManager() 


class ReadQuestionManager(models.Manager):
    def for_user(self, user):
        return self.filter(user=user)

    def for_question(self, question_id):
        return self.filter(question__id=question_id)


class ReadQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = ReadQuestionManager() 
