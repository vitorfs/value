from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from value.workspace.models import Instance, InstanceItem

@login_required
def index(request):
    instances = Instance.objects.all()
    finished_instances = instances.filter(status=Instance.FINISHED).order_by('-updated_at')
    wip_instances = instances.exclude(status=Instance.FINISHED).order_by('-updated_at')
    return render(request, 'workspace/index.html', { 'finished_instances' : finished_instances, 'wip_instances' : wip_instances })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def new(request):
    if request.method == 'POST':
        instance = Instance()
        instance.name = request.POST.get('name')
        instance.description = request.POST.get('description')
        instance.manager = request.user
        instance.created_by = request.user
        instance.save()

        users_id = request.POST.getlist('stakeholders')
        instance.stakeholders = User.objects.filter(pk__in=users_id)
        instance.save()

        items_names = request.POST.getlist('instance_item')
        for name in items_names:
            item = InstanceItem()
            item.instance = instance
            item.name = name
            item.save()

        messages.success(request, u'The value project {0} was added successfully.'.format(instance.name))
        return redirect(reverse('workspace:index'))
    users = User.objects.filter(is_active=True).exclude(pk=request.user.pk)
    return render(request, 'workspace/new.html', { 'users' : users })

@login_required
def instance(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    return render(request, 'workspace/instance.html', { 'instance' : instance })
