from pyexpat import model
from rest_framework import serializers
from exam.models import Exam

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