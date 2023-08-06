"""Test Mapz class."""

from mapz.mapz import Mapz

import pytest


@pytest.fixture
def data():
    """Provide common dict data structure for tests."""

    return {
        "databases": {
            "db1": {
                "host": "localhost",
                "port": 5432,
            },
        },
        "users": [
            "Duhast",
            "Valera",
        ],
        "Params": [
            {"ttl": 120, "flush": True},
            {frozenset({1, 2}): {1, 2}},
        ],
        "name": "Boris",
    }


def test_constructor(data):
    """Test correct instance creation."""

    assert Mapz(data) == data

    assert Mapz({}, data, {}) == data

    assert Mapz(db__conn__host="1.2.3.4") == {
        "db": {"conn": {"host": "1.2.3.4"}}
    }


def test_get(data):
    """Test data access methods."""

    m = Mapz(data)

    assert m["databases"]["db1"]["host"] == "localhost"
    assert m["databases.db1.host"] == "localhost"
    assert m.databases.db1.host == "localhost"

    assert m["databases"].db1.host == "localhost"
    assert m.databases["db1"].host == "localhost"
    assert m.databases.db1["host"] == "localhost"
    assert m["databases.db1"].host == "localhost"
    assert m.databases["db1.host"] == "localhost"


def test_get_nondefault(data):
    """Test data access methods with non-existent keys."""

    m = Mapz(data)

    assert m.get("nonexistent") == Mapz()
    assert m.get("theother", default=None) is None
    assert m.theother == Mapz()


def test_set(data):
    """Test setting the value as 'set' method."""

    m = Mapz(data)

    m.set("users", ["Onotole"])
    assert m.users == ["Onotole"]

    m.set("databases.db1.host", {"direct": "1.2.3.4", "loop": "127.0.0.1"})
    assert m.databases.db1.host.loop == "127.0.0.1"

    assert (
        # fmt: off
        m.set(
            "databases_db1_host_loop", "172.0.0.1", key_sep="_"
        ).databases.db1.host.loop == "172.0.0.1"
        # fmt: on
    )


def test_set_item(data):
    """Test setting the value using subscript method."""

    m = Mapz(data)

    m["users"] = ["Onotole"]
    assert m.users == ["Onotole"]

    m["databases.db1.host"] = {"direct": "1.2.3.4", "loop": "127.0.0.1"}
    assert m.databases.db1.host.loop == "127.0.0.1"

    m["databases.db1.host.loop"] = "172.0.0.1"
    assert m.databases.db1.host.loop == "172.0.0.1"


def test_set_attr(data):
    """Test setting the value using attributes."""

    m = Mapz(data)

    m.users = ["Onotole"]
    assert m.users == ["Onotole"]

    m.databases.db3.host.direct = "1.2.3.4"
    m.databases.db3.host.loop = "127.0.0.1"
    assert m.databases.db3.host.loop == "127.0.0.1"

    m.databases.db3.host.loop = "172.0.0.1"
    assert m.databases.db3.host.loop == "172.0.0.1"


def test_update(data):
    """Test that update overwrites the field."""

    m = Mapz(data)

    assert m.update({"users": None}).users is None


def test_submerge(data):
    """Test submerge method."""

    m = Mapz(data)

    m.submerge({"databases.db2.status": "OFF"}, key_sep=".")
    assert m.databases.db2.status == "OFF"


def test_shallow_copy(data):
    """Test shallow copying."""

    from copy import copy

    m = Mapz(data)
    shallow1 = copy(m)
    shallow2 = m.copy()

    assert m.databases.db1.host == "localhost"
    m.databases.db1.host = "172.31.0.4"
    assert m.databases.db1.host == "172.31.0.4"
    assert shallow1.databases.db1.host == "172.31.0.4"
    assert shallow2.databases.db1.host == "172.31.0.4"

    assert m.name == "Boris"
    m.name = "Dorian"
    assert m.name == "Dorian"
    assert shallow1.name == "Boris"
    assert shallow2.name == "Boris"


def test_deep_copy(data):
    """Test deep copying."""

    from copy import deepcopy

    m = Mapz(data)
    deep1 = deepcopy(m)
    deep2 = m.deepcopy()

    assert m.databases.db1.port == 5432
    m.databases.db1.port = 1234
    assert m.databases.db1.port == 1234
    assert deep1.databases.db1.port == 5432
    assert deep2.databases.db1.port == 5432


def test_lower(data):
    """Test changing keys to lowercase."""

    m = Mapz(data)
    low = m.lower()

    assert m["Params.0.ttl"] == 120
    assert low["params.0.ttl"] == 120
    assert m.lower(inplace=True).params[0].ttl == 120


def test_upper(data):
    """Test changing keys to uppercase."""

    m = Mapz(data)
    up = m.upper()

    assert m.name == "Boris"
    assert up.NAME == "Boris"
    assert m.upper(inplace=True).NAME == "Boris"


def test_flatten(data):
    """Test flattening dict structure."""

    m = Mapz(data)
    flat = m.flatten(prefix="f_")

    assert flat.f_name == "Boris"
    assert flat["f_databases.db1.host"] == "localhost"


def test_to_dict(data):
    """Test conversion to plain dict."""

    def keypartswap(*args, **kwargs):
        """Swap first part of string key with its seconds part."""

        k, v = args
        if k:
            k = str(k)
            length = len(k) // 2
            k = k[length:] + k[:length]

        return k, v

    m = Mapz(data)
    m.map(keypartswap, inplace=True)

    assert m.mena == "Boris"
    assert m.basesdata.b1d.stho == "localhost"

    result = m.map()

    m.basesdata.b1d.stho = "127.0.0.1"
    assert result.basesdata.b1d.stho == "localhost"


def test_to_table(data):
    """Test conversion to printable table."""

    m = Mapz(data)
    _, rows = m.to_table()

    assert rows == [
        ["Params", ""],
        ["  - flush", "True"],
        ["    ttl", "120"],
        ["  - frozenset({1, 2})", "{1, 2}"],
        ["databases", ""],
        ["  db1", ""],
        ["    host", "localhost"],
        ["    port", "5432"],
        ["name", "Boris"],
        ["users", ""],
        ["  -", "Duhast"],
        ["  -", "Valera"],
    ]
