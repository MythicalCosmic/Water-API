from rest_framework.permissions import BasePermission


class GroupPermission(BasePermission):
    def has_permission(self, request, view):
        required_permissions = getattr(view, 'required_permissions', [])
        if request.user.is_superuser:
            return True
        if request.user.user_permissions.filter(codename__in=required_permissions).exists():
            return True
        user_groups_permissions = request.user.groups.values_list('permissions__codename', flat=True)
        if any(perm in required_permissions for perm in user_groups_permissions):
            return True
        return False


