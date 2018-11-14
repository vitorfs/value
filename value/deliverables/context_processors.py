from .models import Deliverable


def deliverable_admin(request):
    context = {'is_deliverable_admin': False}
    if hasattr(request, 'resolver_match'):
        if request.resolver_match is not None:
            deliverable_id = request.resolver_match.kwargs.get('deliverable_id')
            try:
                deliverable = Deliverable.objects.get(pk=deliverable_id)
                if deliverable.manager == request.user or deliverable.admins.filter(pk=request.user.pk).exists():
                    context['is_deliverable_admin'] = True
            except Deliverable.DoesNotExist:
                pass
    return context
