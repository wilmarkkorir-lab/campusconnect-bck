from rest_framework.permissions import BasePermission
from .models import Role


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in [Role.SUPER_ADMIN, Role.UNIVERSITY_ADMIN]:
            return True
        return obj == request.user or getattr(obj, 'user', None) == request.user


class IsLecturer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.LECTURER


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.STUDENT


class IsClassRep(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.CLASS_REP


class IsStudentLeader(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            Role.STUDENT_LEADER, Role.CLUB_LEADER, Role.CLASS_REP
        ]


class IsDeptAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            Role.DEPT_ADMIN, Role.UNIVERSITY_ADMIN, Role.SUPER_ADMIN
        ]


class IsUniversityAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            Role.UNIVERSITY_ADMIN, Role.SUPER_ADMIN
        ]


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.SUPER_ADMIN


class IsLecturerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            Role.LECTURER, Role.DEPT_ADMIN, Role.UNIVERSITY_ADMIN, Role.SUPER_ADMIN
        ]
