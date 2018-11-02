from django.db import models

# Create your models here.
class DjangoBoard(models.Model):
    id = models.IntegerField(primary_key=True)
    subject = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    created_date = models.DateTimeField(null=False)
    mail = models.CharField(max_length=50, blank=True)
    memo = models.CharField(max_length=200, blank=True)
    hits = models.IntegerField(null=True, blank=True)

    # 데이터베이스 만들때 파일과 경로를 담는 파일을 따로 만들어 주는게 좋다.

    file = models.CharField(max_length=100, blank=True)
    place = models.CharField(max_length=150, blank=True)


    def __str__(self):
        return self.subject
