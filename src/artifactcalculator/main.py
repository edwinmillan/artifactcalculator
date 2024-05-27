import re
from pathlib import Path

import click


def load_file(path: str) -> list[str]:
    with open(Path(path), "r") as f:
        data = f.readlines()
        return [line.strip() for line in data if line]


def extract_power_components(line: str) -> list[list[int, int]]:
    components = []
    artifact_power_pattern = re.compile(r"^\(\d+\)")
    pp_pattern = re.compile(r"(\d+) Lvl\. (\d+)")

    if artifact_power_pattern.match(line):
        line_components = pp_pattern.findall(line)
        for component in line_components:
            components.append([int(component[0]), int(component[1])])
    return components


def parse_lines(lines: list[str]) -> list[int]:
    output = []
    conversion_table = {
        1: 1,
        2: 2,
        3: 4,
        4: 8,
        5: 16,
    }
    for line in lines:
        components = extract_power_components(line)
        compound = len(components) > 1
        compounded_pp = []
        for component in components:
            pp, level = component
            l1_pp = pp * conversion_table.get(level, 0)
            if compound:
                compounded_pp.append(l1_pp)
            else:
                output.append(l1_pp)
        if compounded_pp:
            output.append(sum(compounded_pp))
    return output


def total_data(data: list[int]) -> int:
    return sum(data)


def rank_artifact(total_l1_pp: int) -> str:
    ranks = [
        {"range": (1, 200), "rank": "Level 1"},
        {"range": (201, 300), "rank": "Level 1+"},
        {"range": (301, 1200), "rank": "Level 2"},
        {"range": (1201, 1640), "rank": "Level 2+"},
        {"range": (1641, 1760), "rank": "Level 3"},
        {"range": (1761, 4620), "rank": "Level 3+"},
        {"range": (4621, 5880), "rank": "Level 4"},
        {"range": (5881, 5900), "rank": "Level 4+"},
        {"range": (5901, 99999999), "rank": "Level 5"},
    ]

    for rank in ranks:
        min_val, max_val = rank["range"]
        if min_val <= total_l1_pp <= max_val:
            return rank["rank"]

    return "Out of Range"


def main(filepath: str):
    data = load_file(filepath)
    parsed_data = parse_lines(data)
    total_pp = total_data(parsed_data)
    artifact_rank = rank_artifact(total_pp)
    click.echo(f"{artifact_rank} ({total_pp})")


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
def cli(filepath: str):
    main(filepath)


if __name__ == "__main__":
    cli()
