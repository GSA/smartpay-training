import pytest
from training import schemas, models
from training.repositories import AgencyRepository


def test_create(agency_repo_empty: AgencyRepository, valid_agency):
    result = agency_repo_empty.create(valid_agency)
    assert result.id
    assert result.name == valid_agency.name


def test_create_duplicate(agency_repo_with_data: AgencyRepository, valid_agency):
    with pytest.raises(Exception):
        agency_repo_with_data.create(valid_agency)


def test_find_by_name(agency_repo_with_data: AgencyRepository, valid_agency):
    result = agency_repo_with_data.find_by_name(valid_agency)
    assert result is not None
    assert result.name == valid_agency.name


def test_find_by_nonexistent_name(agency_repo_empty: AgencyRepository):
    invalid_agency = schemas.AgencyCreate(name="Nonexistent Agency", bureau=None)
    result = agency_repo_empty.find_by_name(invalid_agency)
    assert result is None


def test_save(agency_repo_empty: AgencyRepository, valid_agency):
    result = agency_repo_empty.save(models.Agency(name=valid_agency.name, bureau=valid_agency.bureau))
    assert result.id
    retrieved_result = agency_repo_empty.find_by_id(result.id)
    assert retrieved_result is not None
    assert retrieved_result.name == valid_agency.name and retrieved_result.bureau == valid_agency.bureau


def test_find_by_id(agency_repo_empty: AgencyRepository, valid_agency):
    agency_id = agency_repo_empty.save(models.Agency(name=valid_agency.name, bureau=valid_agency.bureau)).id
    result = agency_repo_empty.find_by_id(agency_id)
    assert result is not None
    assert result.name == valid_agency.name


def test_find_by_nonexistent_id(agency_repo_empty: AgencyRepository, valid_agency):
    agency_id = agency_repo_empty.save(models.Agency(name=valid_agency.name, bureau=valid_agency.bureau)).id
    result = agency_repo_empty.find_by_id(agency_id + 1)
    assert result is None


def test_find_all(agency_repo_with_data: AgencyRepository, testdata: dict):
    result = agency_repo_with_data.find_all()
    names = list(map(lambda r: r.name, result))
    bureaus = list(map(lambda r: r.bureau, result))
    for item in testdata["agencies"]:
        assert item["name"] in names and item["bureau"] in bureaus


def test_delete_by_id(agency_repo_empty: AgencyRepository, valid_agency):
    agency_id = agency_repo_empty.save(models.Agency(name=valid_agency.name, bureau=valid_agency.bureau)).id
    agency_repo_empty.delete_by_id(agency_id)
    assert agency_repo_empty.find_by_id(agency_id) is None


def test_get_agencies_with_bureaus_sort_order(agency_repo_with_data: AgencyRepository):
    agencies = agency_repo_with_data.get_agencies_with_bureaus()
    last_agency = agencies[-1]
    assert last_agency['name'] == 'Other'
    all_but_last = agencies[:-1]

    assert all(a1['name'] < a2['name'] for a1, a2 in zip(all_but_last, all_but_last[1:]))


def test_get_agencies_with_bureaus_bureau_sort_order(agency_repo_with_data: AgencyRepository):
    agencies = agency_repo_with_data.get_agencies_with_bureaus()
    for agency in agencies:
        if any(b['name'] == 'Other' for b in agency['bureaus']):
            last_bureau = agency['bureaus'][-1]
            assert last_bureau['name'] == 'Other'
            all_but_last_bureau = agency['bureaus'][:-1]
            assert all(b1['name'] < b2['name'] for b1, b2 in zip(all_but_last_bureau, all_but_last_bureau[1:]))
        else:
            assert all(b1['name'] < b2['name'] for b1, b2 in zip(agency['bureaus'], agency['bureaus'][1:]))
