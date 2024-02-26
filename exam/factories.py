import factory
from .models import Question, Exam
from users.models import User
from teachers . models import Subject
from  datetime import timedelta


# class UserFactory(factory.django.DjangoModelFactory):
#     # A factory class for the User model
#     class Meta:
#         model = User
    
#     username = factory.Faker('user_name')
#     email = factory.Faker('email')
#     is_teacher = True # Only create teacher users

# class SubjectFactory(factory.django.DjangoModelFactory): # A factory class for the Subject model 
#     class Meta: 
#         model = Subject # Specify the model to use

#     name = factory.Faker('word') # Generate a random word as the name
#     teacher = factory.SubFactory(UserFactory) # Create a teacher user for each subject
#     assigned = factory.Faker('boolean') # Generate a random boolean value as the assigned status

# class ExamFactory(factory.django.DjangoModelFactory):
#     # A factory class for the Exam model
#     class Meta:
#         model = Exam
    
#     name = factory.Faker('sentence')
#     subject = factory.SubFactory(SubjectFactory)
#     duration = timedelta(minutes=60)
#     start_date = factory.Faker('date')  

class QuestionFactory(factory.django.DjangoModelFactory):
    # A factory class for the Question model
    class Meta:
        model = Question
    
    subject = factory.Iterator(Subject.objects.filter(id=5)) # Create a teacher user for each question
    # exam = factory.Iterator(Exam.objects.filter(id=5)) # Create an exam for each question
    question = factory.Faker('paragraph')
    option_A = factory.Faker('sentence')
    option_B = factory.Faker('sentence')
    option_C = factory.Faker('sentence')
    option_D = factory.Faker('sentence')
    answer = factory.Iterator(['A', 'B', 'C', 'D']) # Randomly choose an answer from the options
    
    
# question_obj = QuestionFactory.build()

# # Create and save a question object with random data
# question = QuestionFactory.create()

# # Create and save a question object with a specific teacher id and exam id
# question = QuestionFactory.create(teacher_id=2, exam_id=3)

# Create a batch of 70 questions with teacher_id=2 and exam_id=3 and the same question and answer
# questions = QuestionFactory.create_batch(70, teacher_id=2, exam_id=3, question="What is the capital of Nigeria?", answer="A")

# # Create a batch of 70 questions with teacher_id=2 and exam_id=3 and random questions and answers
# questions = QuestionFactory.create_batch(70, teacher_id=2, exam_id=3, question=factory.Faker('sentence'), answer=factory.Iterator(['A', 'B', 'C', 'D']))



# # Create and save a list of 10 questions with random data
# questions = QuestionFactory.create_batch(10)
# questions = QuestionFactory.create_batch(5, subject_id=2, exam_id=3)