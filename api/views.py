from functools import partial
import re
import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from school.models import Grade, Term
from .serializers import *
from exam.models import Exam, StudentResult
from users.models import User
from django.db.models import Q
from django.utils import timezone
from django.db import transaction
from rest_framework import status
from django.shortcuts import get_object_or_404
from school.models import AcademicYear, Term, Subject
from django.utils.html import escape
from teachers.views import calculate_positions




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

@api_view(["GET"])
def studentResultData(request):
    grade = request.GET.get("grade")
    academic_year = request.GET.get("academic-year")
    subject = request.GET.get("subject")

    now = timezone.now()

    term = Term.objects.get(start_date__lt =now, end_date__gt=now)
    
    results = StudentResult.objects.filter(academic_year=academic_year, subject=subject, term=term, grade=grade)
    students_without_results = User.objects.filter(
        is_student=True, student__grade=grade, student__status="Approved"
    ).exclude(id__in=results.values_list('student_id', flat=True))

    result_serializers = StudenResultSerialiazer(results, many=True)
    student_without_result_serializers = StudentWithoutResultSerialiazer(students_without_results, many=True)

    # Combine the data from both serializers
    combined_data = (result_serializers.data + student_without_result_serializers.data) 
    return Response(combined_data)   


@api_view(['POST'])
@transaction.atomic
def save_assessment_data(request):
    if request.method == "POST":
        data = request.data
        # Extract academic year, term, subject, and results
        academic_year = data.get('academic_year')
        term = data.get('term')
        subject = data.get('subject')
        grade = data.get('grade')
        students_result = data.get('result')
        
        academic_year  = AcademicYear.objects.get(id=academic_year)
        term = Term.objects.get(id=term)
        subject = Subject.objects.get(id=subject)
        grade = Grade.objects.get(id=grade)


      
        for student in students_result:
            id = student["id"]
            first_cat = student["first_cat"]
            second_cat = student["second_cat"]
            first_test = student["first_test"]
            second_test = student["second_test"]
            exam_score = student["exam_score"]

            if student["student_exist"]:
                try:
                    instance = StudentResult.objects.get(id=id)
                    payload ={"first_cat":first_cat, "second_cat": second_cat, "first_test":first_test, "second_test":second_test, "exam_score":exam_score}
                    serializer = StudenResultSerialiazer(instance, data=payload)
    
                    if serializer.is_valid():
                        serializer.save()
                    else:
                            print("not valid", serializer.errors)
                except StudentResult.DoesNotExist:
                    print("Error")
                # first_cat = student["first_cat"]
                # serializer = StudenResultSerialiazer(data={ "first_cat": first_cat})
            else:
                student= User.objects.get(id=id)
                payload ={
                    "academic_year" : academic_year,
                    "term" : term,
                    "subject" : subject,
                    "grade" : grade,
                    "student":student,
                    "first_cat":first_cat,
                    "second_cat":second_cat,
                    "first_test":first_test,
                    "second_test":second_test,
                    "exam_score":exam_score,
                }
                StudentResult.objects.create(
                    academic_year = academic_year,
                    term = term,
                    subject = subject,
                    grade = grade,
                    student=student,
                    first_cat=first_cat,
                    second_cat=second_cat,
                    first_test=first_test,
                    second_test=second_test,
                    exam_score=exam_score,
                    
                )
            
            calculate_positions(grade, academic_year, subject, term)

    return Response({"message": "Student results saved successfully"}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def save_assessment_data(request):
#     # Parse JSON data from the request body
#     data = request.data
    
#     academic_year = data.get('academic_year')
#     term = data.get('term')
#     subject = data.get('subject')
#     results = data.get('result')

    

#     # Continue with processing the data
#     return Response({"message": "Data saved successfully!"}, status=status.HTTP_200_OK)