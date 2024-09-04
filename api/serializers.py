from pyexpat import model
from turtle import position
from rest_framework import serializers
from exam.models import Exam, StudentResult
from main.decorators import student
from users.models import User

class ExamEventSerializer(serializers.ModelSerializer):
    """calender serializer"""
    title = serializers.CharField(source='name')
    grade = serializers.SerializerMethodField()
    start = serializers.DateTimeField(source='start_date')
    end = serializers.DateTimeField(source='end_date')
    description = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    class Meta:
        model = Exam
        fields = ["id",'title',"grade", "status", 'start', 'end', 'description', "color"]
        
    def get_description(self, obj):
        return f"{obj.get_no_question} question(s)"
    
    def get_color(self, obj):
        status = obj.get_exam_status
        
        return "#f2ff0d" if status == "pending" else "green"
    
    def get_grade(self, obj):
        return obj.grade.grade 
    
    def get_status(self, obj):
        return obj.get_exam_status
    
class ExamSummarySerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields =["id"]


# class StudenResultSerialiazer(serializers.ModelField):
#     """This serializer is used if there a currentyly students data un the database"""
#     student = serializers.ModelSerializer()
#     class Meta:
#         model = StudentResult
#         fields = ["student"]

#     def get_student(self, obj):
#         return obj.get_full_name


class StudenResultSerialiazer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    student_exists = serializers.SerializerMethodField()

    class Meta:
        model = StudentResult
        fields = ['id', 'student',"student_exists", 'first_cat', 'second_cat', 'first_test', 'second_test', 'exam_score', "total_score", "position"]

    def get_student(self, obj):
        return obj.student.get_full_name()
    def get_student_exists(self,obj):
        return True
    
    # def save(self, *args, **kwargs):
    #     # Access the instance being saved
    #     instance = super().save(*args, **kwargs)
        
    #     # Calculate the total score if all components are present
    #     if (instance.exam_score is not None):
    #         instance.total_score = (
    #             (instance.first_cat or 0) +
    #             (instance.second_cat or 0) +
    #             (instance.first_test or 0) +
    #             (instance.second_test or 0) +
    #             (instance.exam_score)
    #         )
    #         instance.save()  # Save the updated instance with the total score

    #     return instance
    

class StudentWithoutResultSerialiazer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    first_cat = serializers.SerializerMethodField()
    second_cat = serializers.SerializerMethodField()
    first_test = serializers.SerializerMethodField()
    second_test = serializers.SerializerMethodField()
    exam_score = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['student',"id",'first_cat', 'second_cat', 'first_test', 'second_test', 'exam_score']

    def get_student(self, obj):
        return obj.get_full_name()

    def get_first_cat(self, obj):
        return ""

    def get_second_cat(self, obj):
        return ""

    def get_first_test(self, obj):
        return ""

    def get_second_test(self, obj):
        return ""

    def get_exam_score(self, obj):
        return ""
    

