from training.repositories import RoleRepository


def test_create(role_repo_empty: RoleRepository, valid_role):

    result = role_repo_empty.create(valid_role)
    assert result is not None
    assert result.name == valid_role.name


def test_find_by_name(role_repo_with_data: RoleRepository, valid_role):
    result = role_repo_with_data.find_by_name(valid_role.name)
    assert result is not None
