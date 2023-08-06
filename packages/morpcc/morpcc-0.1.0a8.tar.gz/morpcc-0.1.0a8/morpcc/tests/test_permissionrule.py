import pytest

from .democms.app import App, AppRoot
from .democms_common import follow, get_democms_client


@App.json(model=AppRoot, name="test-cache")
def cache_test(context, request):
    userid = request.GET.get("userid", request.identity.userid)
    cache_key = str(
        [userid, "morpcc.tests.democms.app:AppRoot", "morpcc.permission:ViewHome",]
    )
    try:
        cache = request.cache.get_cache("morpcc.permission_rule", expire=3600)
        value = cache.get(cache_key)
    except KeyError:
        return {"exists": False}
    return {"exists": True, "value": value}


def test_permissionrule(pgsql_db, pgsql_db_cache):
    c = get_democms_client()
    request = c.mfw_request

    # login as admin
    r = c.post(
        "/login",
        {
            "__formid_": "deform",
            "username": "admin",
            "password": "password",
            "Submit": "Login",
        },
    )

    # create user
    r = c.post(
        "/manage-users/+create",
        {
            "__formid__": "deform",
            "username": "user",
            "email": "user@localhost.localdomain",
            "password": "password",
            "source": "local",
            "timezone": "UTC",
            "is_administrator": "false",
        },
    )

    # get user uuid
    r = c.get("/api/auth/user/+search")
    for i in r.json["results"]:
        if i["data"]["username"] == "user":
            user_uuid = i["data"]["uuid"]

    # logout admin
    r = c.get("/logout")

    # login as user
    r = c.post(
        "/login",
        {
            "__formid_": "deform",
            "username": "user",
            "password": "password",
            "Submit": "Login",
        },
    )

    r = r.follow(expect_errors=True)

    assert r.status_code == 403

    r = c.get("/test-cache?userid=%s" % user_uuid)
    assert r.json["exists"]
    assert not r.json["value"]

    # logout
    r = c.get("/logout")

    # login as admin
    r = c.post(
        "/login",
        {
            "__formid_": "deform",
            "username": "admin",
            "password": "password",
            "Submit": "Login",
        },
    )

    # allow view home
    r = c.post(
        "/permissionassignment/+create",
        (
            ("__formid__", "deform"),
            ("model", "morpcc.root:Root"),
            ("permission", "morpcc.permission:ViewHome"),
            ("__start__", "roles:sequence"),
            ("roles", "__default__::member"),
            ("__end__", "roles:sequence"),
            ("rule", "allow"),
            ("enabled", "true"),
            ("Submit", "submit"),
        ),
    )

    r = c.get("/test-cache?userid=%s" % user_uuid)
    assert not r.json["exists"]
    # logout admin
    r = c.get("/logout")

    # login as user
    r = c.post(
        "/login",
        {
            "__formid_": "deform",
            "username": "user",
            "password": "password",
            "Submit": "Login",
        },
    )

    r = r.follow()

    # logout admin
    r = c.get("/logout")

    # login as user
    r = c.post(
        "/login",
        {
            "__formid_": "deform",
            "username": "user",
            "password": "password",
            "Submit": "Login",
        },
    )

    r = r.follow()

