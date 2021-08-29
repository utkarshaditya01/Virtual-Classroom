from django.db import models
from users.models import Tutor, Student


class Assignment(models.Model):
    STATUS = (('S', 'Scheduled'), ('O', 'Ongoing'))

    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    description = models.TextField()
    published = models.DateTimeField()
    deadline = models.DateTimeField()

    def my_submission(self, user_id):
        try:
            return self.submission_set.get(student_id=user_id)
        except Submission.DoesNotExist:
            return None

    def all_submissions(self):
        return self.submission_set.all()

    def __str__(self):
        return str(self.id) + " " + str(self.description)


class Submission(models.Model):
    STATUS = (('S', 'Submitted'), ('P', 'Pending'))

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=2)
    remark = models.TextField()
    submitted_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + " " + str(self.student) + " " + str(self.assignment)
