import importlib

import morpfw
import rulez

#
from .modelui import PermissionAssignmentCollectionUI, PermissionAssignmentModelUI
from .schema import PermissionAssignmentSchema

#


class PermissionAssignmentModel(morpfw.Model):
    schema = PermissionAssignmentSchema

    #
    def ui(self):
        return PermissionAssignmentModelUI(self.request, self, self.collection.ui())

    #
    def permission_class(self):
        modname, objname = self["permission"].split(":")
        mod = importlib.import_module(modname)
        return getattr(mod, objname)

    def model_class(self):
        modname, objname = self["model"].split(":")
        mod = importlib.import_module(modname)
        return getattr(mod, objname)

    def match(self, obj):
        return isinstance(obj, self.model_class())


class PermissionAssignmentCollection(morpfw.Collection):
    schema = PermissionAssignmentSchema

    #
    def ui(self):
        return PermissionAssignmentCollectionUI(self.request, self)

    #

    @morpfw.requestmemoize()
    def lookup_permission(self, model_name):
        return self.search(
            rulez.and_(
                rulez.field["model"] == model_name, rulez.field["enabled"] == True,
            )
        )

    @morpfw.requestmemoize()
    def all_enabled(self):
        return self.search(rulez.field["enabled"] == True,)
