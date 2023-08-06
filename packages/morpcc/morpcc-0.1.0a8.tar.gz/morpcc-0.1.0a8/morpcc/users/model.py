import os

from morpfw.authn.pas.user.model import UserCollection, UserModel
from morpfw.crud.blobstorage.fsblobstorage import FSBlobStorage

from ..app import App
from ..crud.model import CollectionUI, ModelUI


@App.blobstorage(model=UserModel)
def get_user_blobstorage(model, request):
    return request.app.get_config_blobstorage(request)


class UserModelUI(ModelUI):

    view_exclude_fields = ModelUI.view_exclude_fields + ["password", "nonce"]
    edit_include_fields = ["email", "timezone"]


class UserCollectionUI(CollectionUI):

    modelui_class = UserModelUI

    page_title = "Users"
    listing_title = "Registered Users"
    create_view_enabled = True

    columns = [
        {"title": "Username", "name": "username"},
        {"title": "Created", "name": "created"},
        {"title": "State", "name": "state"},
        {"title": "Source", "name": "source"},
        {"title": "Actions", "name": "structure:buttons"},
    ]


class CurrentUserModelUI(UserModelUI):
    pass


def get_usercol_ui(self):
    return UserCollectionUI(self.request, self)


def get_usermodel_ui(self):
    return UserModelUI(self.request, self, self.collection.ui())


if not hasattr(UserModel, "ui"):
    UserModel.ui = get_usermodel_ui

if not hasattr(UserCollection, "ui"):
    UserCollection.ui = get_usercol_ui

