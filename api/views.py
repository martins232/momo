from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from exam.models import Exam
from django.db.models import Q
from django.utils import timezone



# Create your views here.
@api_view(["GET"])
def examList(request):
    exams = Exam.objects.filter( Q(start_date__gt=timezone.now()) | Q(start_date__lte=timezone.now(), end_date__gt=timezone.now()), teacher=request.user)
    serializers = ExamEventSerializer(exams, many=True)
    return Response(serializers.data)

@api_view(["GET"])
def examSummary(request, pk):
    exams = Exam.objects.filter(grade=pk, teacher=request.user, deleted= False)
    now = timezone.now()
    data = {
        "total_exam": exams.count(),
        "active": exams.filter(start_date__lt=now, end_date__gt=now).count(),
        "pending": exams.filter(start_date__gt=now).count(),
        "ended": exams.filter(end_date__lt=now).count(),
    }
    return Response(data)
    