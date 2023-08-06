from morpfw.crud import permission as crudperms

from ..app import App
from .model import NotificationCollection, NotificationModel


@App.permission_rule(model=NotificationCollection, permission=crudperms.Search)
def collection_search_permission(identity, model, permission):
    if identity.userid:
        return True
    return False


@App.permission_rule(model=NotificationCollection, permission=crudperms.View)
def collection_view_permission(identity, model, permission):
    if identity.userid:
        return True
    return False


@App.permission_rule(model=NotificationModel, permission=crudperms.View)
def model_view_permission(identity, model, permission):
    if identity.userid == model["userid"]:
        return True
    return False
