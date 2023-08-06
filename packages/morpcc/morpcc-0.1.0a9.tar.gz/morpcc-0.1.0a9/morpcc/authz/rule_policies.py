from morpfw.crud import permission as crudperms
from morpfw.crud.model import Collection, Model
from morpfw.permission import All

from .permission_rule import rule_from_assignment


def readonly_policy(groupname, identity, model, permission):
    request = model.request
    users = request.get_collection("morpfw.pas.user")
    user = users.get_by_userid(identity.userid)
    if user["is_administrator"]:
        return True

    if groupname not in [g["groupname"] for g in user.groups()]:
        return False

    if isinstance(model, Collection):
        if issubclass(permission, crudperms.View):
            return True
        if issubclass(permission, crudperms.Search):
            return True
    elif isinstance(model, Model):
        if issubclass(permission, crudperms.View):
            return True
    return False

def full_access_policy(groupname, identity, model, permission):
    request = model.request
    users = request.get_collection("morpfw.pas.user")
    user = users.get_by_userid(identity.userid)
    if user["is_administrator"]:
        return True

    if groupname not in [g["groupname"] for g in user.groups()]:
        return False

    if issubclass(permission, All):
        return True

    return False
   

def content_submission_policy(groupname, identity, model, permission):
    request = model.request
    users = request.get_collection("morpfw.pas.user")
    user = users.get_by_userid(identity.userid)
    if user["is_administrator"]:
        return True

    if groupname not in [g["groupname"] for g in user.groups()]:
        return False

    if isinstance(model, Collection):
        if issubclass(permission, crudperms.View):
            return True
        if issubclass(permission, crudperms.Search):
            return True
        if issubclass(permission, crudperms.Create):
            return True
    elif isinstance(model, Model):
        if model["creator"] != user.uuid:
            return False

        if issubclass(permission, crudperms.All):
            return True

        if issubclass(permission, crudperms.StateUpdate):
            return True
    return False


def content_approval_policy(groupname, identity, model, permission):
    request = model.request
    users = request.get_collection("morpfw.pas.user")
    user = users.get_by_userid(identity.userid)
    if user["is_administrator"]:
        return True

    if groupname not in [g["groupname"] for g in user.groups()]:
        return False

    if isinstance(model, Collection):
        if issubclass(permission, crudperms.View):
            return True
        if issubclass(permission, crudperms.Search):
            return True

    elif isinstance(model, Model):
        if issubclass(permission, crudperms.View):
            return True

        if issubclass(permission, crudperms.Edit):
            return True

        if issubclass(permission, crudperms.StateUpdate):
            return True
    return False

