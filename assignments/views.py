from assignments.serializers import *
from rest_framework import views
from users.permissions import IsTutor, IsStudent
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi


class CreateAssignment(views.APIView):
    permission_classes = [IsTutor]

    @swagger_auto_schema(request_body=AssignmentSerializer, responses={200: "Successfully Created Assignment", 403: "Only tutors can create assignment.", 404: "Bad Request"}, operation_summary="Create Assignment")
    def post(self, request):
        print(request.data)  # ask
        serializer = AssignmentSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            assignment = serializer.save()
        else:
            return Response(serializer.errors)
        data = {'message': "Successfully Created Assignment"}
        return Response(data, status=status.HTTP_200_OK)


class UpdateDeleteAssignment(views.APIView):
    permission_classes = [IsTutor]

    @swagger_auto_schema(responses={200: "Successfully Deleted Assignment", 404: "Bad Request"}, operation_summary="Delete Assignment")
    def delete(self, request, id):
        try:
            assignment = Assignment.objects.get(id=id)
            assignment.delete()
            data = {'message': "Successfully Deleted Assignment"}
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(status=404)

    @swagger_auto_schema(request_body=AssignmentSerializer, responses={200: "Successfully Updated Assignment", 403: "Only tutors can update assignment.", 404: "Bad Request"}, operation_summary="Update Assignment")
    def put(self, request, id):
        try:
            assignment = Assignment.objects.get(id=id)
            serializer = AssignmentSerializer(
                assignment, data=request.data, partial=True)

            if serializer.is_valid():
                assignment = serializer.save()
                data = {'message': "Successfully Updated Assignment"}
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors)
        except:
            return Response(status=404)

# noinspection PyMethodMayBeStatic


class SubmitAssignment(views.APIView):
    permission_classes = [IsStudent]

    @swagger_auto_schema(request_body=SubmissionUpdateSerializer, responses={200: AssignmentDetailStudentSerializer, 403: "Only students can submit.", 404: "Bad Request"}, operation_summary="Create Submission")
    def post(self, request, assignment_id):
        try:
            assignment = Assignment.objects.get(id=assignment_id)
            #submission = Submission.objects.filter(assignment=assignment).filter(student = request.user.student).first()
            submission = assignment.my_submission(request.user.id)
            serializer = SubmissionUpdateSerializer(
                submission, data=request.data, partial=True)
            # ask this ^^
            if serializer.is_valid():
                submission = serializer.save()
                return Response(AssignmentDetailStudentSerializer(assignment, context={'user_id': request.user.id}).data)
            else:
                return Response(serializer.errors)
        except Assignment.DoesNotExist:
            return Response(status=404)


class AssignmentDetails(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: AssignmentDetailStudentSerializer, 404: "No such assignment"}, operation_summary="Assignment Details")
    def post(self, request, assignment_id):
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            return Response(status=404)

        if hasattr(request.user, 'tutor') and request.user.tutor:
            serializer = AssignmentDetailTutorSerializer(assignment)
            return Response(serializer.data)
        if hasattr(request.user, 'student') and request.user.student:
            serializer = AssignmentDetailStudentSerializer(
                assignment, context={'user_id': request.user.id})
            return Response(serializer.data)


class AssigmentFeed(views.APIView):
    permission_classes = [IsAuthenticated]
    response_schema = openapi.Schema(
        'Assignment Feed', type=openapi.TYPE_ARRAY,

        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tutor': openapi.Schema(title='Name & email of Tutor', type=openapi.TYPE_STRING),
                'description': openapi.Schema(title='Assignment Description', type=openapi.TYPE_STRING),
                'published': openapi.Schema(title='Published Date', type=openapi.TYPE_STRING,
                                            format=openapi.FORMAT_DATE),
                'deadline': openapi.Schema(title='Submission Deadline', type=openapi.TYPE_STRING,
                                           format=openapi.FORMAT_DATE),
                'all_submissions': openapi.Schema(
                    title='Submissions', description='Available Only for Tutors',
                    type=openapi.TYPE_ARRAY, items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'remark': openapi.Schema(title='Remark',
                                                     type=openapi.TYPE_STRING),
                            'status': openapi.Schema(title='Remark',
                                                     type=openapi.TYPE_STRING,
                                                     enum=['Pending',
                                                           'Submitted']),
                            'submitted_on': openapi.Schema(
                                title='Submitted on',
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_DATE),
                            'student': openapi.Schema(
                                title='Student Name & email',
                                type=openapi.TYPE_STRING)
                        })),
                'my_submission': openapi.Schema(
                    title='My Submission',
                    description='Only for student',
                    type=openapi.TYPE_OBJECT,
                    properties={'remark': openapi.Schema(title='Remark', type=openapi.TYPE_STRING),
                                'status': openapi.Schema(title='Remark', type=openapi.TYPE_STRING,
                                                         enum=['Pending', 'Submitted']),
                                'submitted_on': openapi.Schema(title='Submitted on',
                                                               type=openapi.TYPE_STRING,
                                                               format=openapi.FORMAT_DATE),
                                })

            }, required=['tutor', 'description', 'published', 'deadline']))

    @swagger_auto_schema(responses={200: response_schema}, operation_summary="Assignment Feed",
                         manual_parameters=[openapi.Parameter('publishedAt', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['ONGOING', 'SCHEDULED']),
                         openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['ALL', 'PENDING', 'OVERDUE', 'SUBMITTED'], description="Only for students, does not filter for tutor.")])
    def get(self, request):
        published_at = request.GET.get('publishedAt')
        print(request.user)
        status = request.GET.get('status')
        if hasattr(request.user, 'student') and request.user.student:
            assignments = Assignment.objects.all()
        elif hasattr(request.user, 'tutor') and request.user.tutor:
            assignments = Assignment.objects.filter(tutor=request.user.tutor)
        else:
            return Response(status=403)

        if published_at == 'ONGOING':
            assignments = assignments.filter(
                deadline__gt=datetime.now(), published__lt=datetime.now())
        elif published_at == 'SCHEDULED':
            assignments = assignments.filter(published__gt=datetime.now())
        if hasattr(request.user, 'student') and request.user.student:
            if status == 'ALL':
                pass
            elif status == 'PENDING':
                assignments = assignments.filter(
                    submission__status='P', submission__student=request.user.student, deadline__gt=datetime.now())
                print(assignments)
            elif status == 'OVERDUE':
                assignments = assignments.filter(
                    submission__status='P', submission__student=request.user.student, deadline__lt=datetime.now() )
            elif status == 'SUBMITTED':
                assignments = assignments.filter(submission__status='S', submission__student=request.user.student)

        if hasattr(request.user, 'tutor') and request.user.tutor:
            serializer = AssignmentDetailTutorSerializer(
                assignments, many=True)
            return Response(serializer.data)
        if hasattr(request.user, 'student') and request.user.student:
            serializer = AssignmentDetailStudentSerializer(
                assignments, many=True, context={'user_id': request.user.id})
            return Response(serializer.data)

        return Response([])
