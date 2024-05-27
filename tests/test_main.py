import pytest

from src.artifactcalculator.main import (
    extract_power_components,
    load_file,
    parse_lines,
    rank_artifact,
    total_data,
)


@pytest.mark.parametrize(
    "line, expected",
    [
        ("(10) Offensive Facet: Increased Damage (+10, 20 Lvl. 1 PP)", [[20, 1]]),
        (
            "(15) Defensive Facet: Defensive Empowerment (+10, 120 Lvl. 2 PP)",
            [[120, 2]],
        ),
        ("(25) Offensive Facet: Offensive Empowerment (+15, 60 Lvl. 3 PP)", [[60, 3]]),
        (
            "(25) Offensive Facet: Special Attack: Lightning Palm (800 Ft Range, Max Damage, 80ft Radius, 80 Lvl. 2 PP, 80 Lvl. 3 PP)",
            [[80, 2], [80, 3]],
        ),
    ],
)
def test_extract_power_components(line, expected):
    assert extract_power_components(line) == expected


@pytest.mark.parametrize(
    "lines,expected",
    [
        (
            [
                "(10) Offensive Facet: Increased Damage (+10, 20 Lvl. 1 PP)",
                "(15) Defensive Facet: Defensive Empowerment (+10, 120 Lvl. 2 PP)",
                "(25) Offensive Facet: Offensive Empowerment (+15, 60 Lvl. 3 PP)",
                "(25) Offensive Facet: Special Attack: Lightning Palm (800 Ft Range, Max Damage, 80ft Radius, 80 Lvl. 2 PP, 80 Lvl. 3 PP)",
            ],
            [20, 240, 240, 480],
        ),
    ],
)
def test_parse_lines(lines: list[str], expected: list[int]):
    assert parse_lines(lines) == expected


def test_sample_data():
    path = "tests/test_artifact.md"
    data = load_file(path)
    assert isinstance(data, list)
    assert (
        data[-1]
        == "(15) Offensive Facet: Improved Critical (+20 Critical, 40 Lvl. 2 PP)"
    )


def test_parse_file():
    path = "tests/test_artifact.md"
    data = load_file(path)
    parsed_data = parse_lines(data)
    assert parsed_data == [240, 200, 600, 480, 320, 80]


@pytest.mark.parametrize("data,expected", [([240, 200, 600, 480, 320, 80], 1920)])
def test_total_data(data, expected):
    assert total_data(data) == expected


@pytest.mark.parametrize(
    "total_l1_pp,expected",
    [
        (0, "Out of Range"),
        (200, "Level 1"),
        (300, "Level 1+"),
        (1200, "Level 2"),
        (1600, "Level 2+"),
        (1700, "Level 3"),
        (1920, "Level 3+"),
        (5000, "Level 4"),
        (5890, "Level 4+"),
        (7000, "Level 5"),
        (999999999, "Out of Range"),
    ],
)
def test_rank_artifact(total_l1_pp, expected):
    assert rank_artifact(total_l1_pp) == expected
