import importlib

import morpfw

#
from .modelui import (
    ObjectPermissionAssignmentCollectionUI,
    ObjectPermissionAssignmentModelUI,
)
from .schema import ObjectPermissionAssignmentSchema

#


class ObjectPermissionAssignmentModel(morpfw.Model):
    schema = ObjectPermissionAssignmentSchema

    #
    def ui(self):
        return ObjectPermissionAssignmentModelUI(
            self.request, self, self.collection.ui()
        )

    #
    def permission_class(self):
        modname, objname = self["permission"].split(":")
        mod = importlib.import_module(modname)
        return getattr(mod, objname)

    def match(self, obj):
        return self["object_uuid"] == obj.uuid


class ObjectPermissionAssignmentCollection(morpfw.Collection):
    schema = ObjectPermissionAssignmentSchema

    #
    def ui(self):
        return ObjectPermissionAssignmentCollectionUI(self.request, self)


#

