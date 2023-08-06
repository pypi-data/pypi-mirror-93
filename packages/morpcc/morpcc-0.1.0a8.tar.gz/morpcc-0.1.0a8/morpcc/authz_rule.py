from .app import App
from .permission import EditOwnProfile, SiteSearch, ViewHome
from .root import Root


@App.authz_rule(name="morpcc.basic")
def group_rule(groupname, identity, model, permission):
    request = model.request
    users = request.get_collection("morpfw.pas.user")
    user = users.get_by_userid(identity.userid)
    if user["is_administrator"]:
        return True

    if groupname not in [g["groupname"] for g in user.groups()]:
        return False

    if isinstance(model, Root):
        if (
            issubclass(permission, EditOwnProfile)
            or issubclass(permission, SiteSearch)
            or issubclass(permission, ViewHome)
        ):
            return True
    return False
