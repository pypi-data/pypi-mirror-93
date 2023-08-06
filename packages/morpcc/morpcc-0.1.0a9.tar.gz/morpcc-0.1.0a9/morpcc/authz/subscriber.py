from morpfw.crud import model, signals

from ..app import App
from ..objectpermissionassignment.model import ObjectPermissionAssignmentModel
from ..permissionassignment.model import PermissionAssignmentModel


def _clear(request):
    cache = request.cache.get_cache("morpcc.permission_rule", expire=3600)
    cache.clear()


@App.subscribe(signal=signals.OBJECT_CREATED, model=PermissionAssignmentModel)
def created(app, request, obj, signal):
    _clear(request)


@App.subscribe(signal=signals.OBJECT_UPDATED, model=PermissionAssignmentModel)
def updated(app, request, obj, signal):
    _clear(request)


@App.subscribe(signal=signals.OBJECT_TOBEDELETED, model=PermissionAssignmentModel)
def deleted(app, request, obj, signal):
    _clear(request)


@App.subscribe(signal=signals.OBJECT_CREATED, model=ObjectPermissionAssignmentModel)
def op_created(app, request, obj, signal):
    _clear(request)


@App.subscribe(signal=signals.OBJECT_UPDATED, model=ObjectPermissionAssignmentModel)
def op_updated(app, request, obj, signal):
    _clear(request)


@App.subscribe(signal=signals.OBJECT_TOBEDELETED, model=ObjectPermissionAssignmentModel)
def op_deleted(app, request, obj, signal):
    _clear(request)
