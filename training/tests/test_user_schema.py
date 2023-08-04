from .factories import UserSchemaFactory, RoleSchemaFactory


def test_is_admin_with_admin_user():
    admin_role = RoleSchemaFactory.build(name="Admin")
    admin_user = UserSchemaFactory.build(roles=[admin_role])
    assert admin_user.is_admin()


def test_is_admin_with_nonadmin_user():
    regular_user = UserSchemaFactory.build()
    assert not regular_user.is_admin()
