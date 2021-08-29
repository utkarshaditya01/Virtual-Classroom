from rest_framework.permissions import IsAuthenticated


class IsTutor(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if hasattr(request.user, 'tutor') and request.user.tutor:
            return True
        return False


class IsStudent(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if hasattr(request.user, 'student') and request.user.student:
            return True
        return False
