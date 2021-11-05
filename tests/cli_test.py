"""Unit tests for `usql_conf`."""
from pathlib import Path

import pytest

from usql_conf import cli


@pytest.mark.parametrize(
    ["input", "expected"],
    [
        [
            ["pg_test"],
            "pg://test_user:password123@localhost/test_database?sslmode=disable\n",
        ],
        [["my_test"], "my://test_user:password123@127.0.0.1:3306/some_db\n"],
        [["ms_test"], "ms://mr_tests:abc123@host/dbname\n"],
    ],
)
def test_main(input, expected, capsys, mocker):
    """Main returns expected outputs when valid config name is supplied."""
    mocker.patch(
        "usql_conf.cli.Path.home",
        return_value=Path(__file__).parent / "mock_home",
    )
    mocker.patch(
        "usql_conf.cli.Path.cwd",
        return_value=Path(__file__).parent / "mock_cwd",
    )

    assert not cli.main(input)

    out, err = capsys.readouterr()

    assert out == expected
    assert err == ""


@pytest.mark.parametrize(["input"], [[["pg_abc"]], [["my_abc"]]])
def test_main_config_name_not_set(input, capsys, mocker):
    """Main returns error when no config name match is found."""
    mocker.patch(
        "usql_conf.cli.Path.home",
        return_value=Path(__file__).parent / "mock_home",
    )
    mocker.patch(
        "usql_conf.cli.Path.cwd",
        return_value=Path(__file__).parent / "mock_cwd",
    )
    assert cli.main(input)

    out, err = capsys.readouterr()

    assert out == ""
    assert err == f"Config '{input[0]}' has not been set in .usql_conf\n"


@pytest.mark.parametrize(
    ["input", "expected"],
    [
        [["pg_test"], "pg://mr_test:abc123@localhost/test_database?sslmode=disable\n"],
        [["my_test"], "my://mr_tests:abc123@127.0.0.1:3306/some_db\n"],
        [["ms_test"], "ms://mr_tests:abc123@host/dbname\n"],
    ],
)
def test_main_home_exist_only(input, expected, capsys, mocker):
    """Connection string returned from `~/.usql_conf` if `./.usql_conf` not exists."""
    mocker.patch(
        "usql_conf.cli.Path.home",
        return_value=Path(__file__).parent / "mock_home",
    )
    mocker.patch("usql_conf.cli.Path.cwd", return_value=Path(__file__).parent)
    assert not cli.main(input)

    out, err = capsys.readouterr()

    assert out == expected
    assert err == ""


@pytest.mark.parametrize(
    ["input", "expected"],
    [
        [
            ["pg_test"],
            "pg://test_user:password123@localhost/test_database?sslmode=disable\n",
        ],
        [["my_test"], "my://test_user:password123@127.0.0.1:3306/some_db\n"],
    ],
)
def test_main_cwd_exist_only(input, expected, capsys, mocker):
    """Connection string returned from `./.usql_conf` if exists."""
    mocker.patch("usql_conf.cli.Path.home", return_value=Path(__file__).parent)
    mocker.patch(
        "usql_conf.cli.Path.cwd",
        return_value=Path(__file__).parent / "mock_cwd",
    )
    assert not cli.main(input)

    out, err = capsys.readouterr()

    assert out == expected
    assert err == ""
