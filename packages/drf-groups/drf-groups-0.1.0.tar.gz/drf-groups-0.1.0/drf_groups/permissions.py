from rest_framework import permissions


class BelongsToGroups(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed_groups = getattr(view, 'allowed_groups', [])
        
        if not len(allowed_groups):
            return True

        matching_user_groups = request.user.groups.filter(name__in=allowed_groups)
        return matching_user_groups.exists()