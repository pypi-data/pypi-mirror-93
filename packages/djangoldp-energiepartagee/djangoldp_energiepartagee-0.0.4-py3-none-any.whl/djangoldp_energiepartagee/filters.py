from djangoldp.filters import LDPPermissionsFilterBackend
from rest_framework_guardian.filters import ObjectPermissionsFilter
from djangoldp.utils import is_anonymous_user


class ContributionFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset

        from .models import Relatedactor
        my_actor_pks = Relatedactor.get_mine(user=request.user, role='admin').values_list('pk', flat=True)
        return queryset.filter(actor_id__in=my_actor_pks)


class ProfileFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        if is_anonymous_user(request.user):
            return view.model.objects.none()
        elif request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user=request.user)


class RelatedactorFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user=request.user)
