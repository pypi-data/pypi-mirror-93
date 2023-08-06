import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import PermissionAssignmentModel


class PermissionAssignment(morpfw.sql.Base):

    __tablename__ = "morpcc_permissionassignment"

    model = sa.Column(sa.String(length=256))
    permission = sa.Column(sa.String(length=256))
    is_creator = sa.Column(sa.Boolean())
    users = sa.Column(sajson.JSONField())
    groups = sa.Column(sajson.JSONField())
    roles = sa.Column(sajson.JSONField())
    rule = sa.Column(sa.String(length=24))
    enabled = sa.Column(sa.Boolean())


class PermissionAssignmentStorage(morpfw.SQLStorage):
    model = PermissionAssignmentModel
    orm_model = PermissionAssignment
