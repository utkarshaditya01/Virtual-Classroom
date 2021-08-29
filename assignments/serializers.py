from rest_framework import serializers
from .models import Submission, Assignment
from users.models import Student
from datetime import datetime


class StudentSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)


class AssignmentSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    class Meta:
        model = Assignment
        extra_kwargs = {'students': {'write_only': True}}
        fields = ['description', 'published', 'deadline', 'students']

    def create(self, validated_data):
        user = self.context['request'].user
        # if (user.is_tutor==False):
        #     raise Exception
        students = validated_data.pop('students')
        assignment = Assignment(**validated_data, tutor=user.tutor)
        assignment.save()
        for s in students:
            try:
                student = Student.objects.get(username=s['username'])
                Submission.objects.create(student=student, assignment=assignment, status='P')
            except Student.DoesNotExist:
                continue
        return assignment

    def update(self, instance, validated_data):
        instance.description = validated_data.get("description", instance.description)
        instance.published = validated_data.get("published", instance.published)
        instance.deadline = validated_data.get("deadline", instance.deadline)
        updated_students = validated_data.get("students")
        updated_students = set(list(map(lambda x: x.get("username"), updated_students)))
        if updated_students:
            for s in updated_students:
                try:
                    student = Student.objects.get(username=s)
                    if not instance.submission_set.filter(student=student).exists():
                        Submission.objects.create(student=student, assignment=instance, status='P')     
                except Student.DoesNotExist:
                    continue  
            for s in instance.submission_set.all():
                if s.student.username not in updated_students:
                    s.delete()
        instance.save()
        return instance


class SubmissionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['remark']

    def update(self, instance, validated_data):
        instance.remark = validated_data.get("remark", instance.remark)
        instance.submitted_on = datetime.now()
        instance.status = 'S'
        instance.save()
        return instance


class SubmissionSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Submission
        fields = ['remark', 'status', 'submitted_on']


class AssignmentDetailStudentSerializer(serializers.ModelSerializer):
    class MySubmissionField(serializers.Field):
        def to_representation(self, obj):
            user_id = self.context.get('user_id')
            try:
                submission = obj.my_submission(user_id)
                return SubmissionSerializer(submission).data
            except Submission.DoesNotExist:
                return None

    tutor = serializers.StringRelatedField()
    my_submission = MySubmissionField(source='*', read_only=True)

    class Meta:
        model = Assignment
        fields = ['tutor', 'description', 'published', 'deadline', 'my_submission']


class TutorSubmissionSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    student = serializers.StringRelatedField()

    class Meta:
        model = Submission
        fields = ['remark', 'status', 'submitted_on', 'student']


class AssignmentDetailTutorSerializer(serializers.ModelSerializer):
    all_submissions = TutorSubmissionSerializer(many=True)
    tutor = serializers.StringRelatedField()

    class Meta:
        model = Assignment
        fields = ['tutor', 'description', 'published', 'deadline', 'all_submissions']


