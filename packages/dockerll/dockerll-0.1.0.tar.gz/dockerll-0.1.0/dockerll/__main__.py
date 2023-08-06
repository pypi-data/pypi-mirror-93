#!/usr/bin/env python

import sys
import subprocess
from typing import Tuple

import click

from dockerll.pattern import (
    make_block_name_pattern,
    make_block_pattern,
    make_block_tag_pattern,
)


def blockify(s):
    block_pattern = make_block_pattern()
    blocks = block_pattern.split(s)[1:]
    it = iter(blocks)
    yield from zip(it, it)


def read_and_output(show_docker: bool):
    for line in sys.stdin:
        if show_docker:
            sys.stdout.write(line)
        yield line


@click.command("main")
@click.option(
    "-r", "--repo",
    required=True,
    help="Docker repository name"
)
@click.option(
    "-t", "--tag", "tags",
    multiple=True,
    help="The stages to tag. Supports \"stage\" and \"stage:tag\""
)
@click.option("-s", "--silence-docker", "show_docker", is_flag=True, default=True)
@click.option("-v", "--verbose", is_flag=True, default=False, show_default=True)
def main(repo: str, tags: Tuple[str, ...], show_docker: bool, verbose: bool):
    tags_map = dict(map(lambda x: x.split(':') if ':' in x else (x, x), tags))
    stream = "".join(read_and_output(show_docker))

    block_name_pattern = make_block_name_pattern()
    for block_name, block_content in blockify(stream):
        stage = block_name_pattern.match(block_name).groupdict()["image_target"]

        block_tag_pattern = make_block_tag_pattern()
        layers = [
            match.groupdict()["layer"]
            for match in block_tag_pattern.finditer(block_content)
        ]

        last_block_layer = layers[-1]

        if stage not in tags_map:
            continue

        stage = tags_map.get(stage, stage)
        tag = f"{repo}:{stage}"

        cmd = ["docker", "tag", last_block_layer, tag]
        process = subprocess.Popen(cmd, stdout=sys.stdout)
        process.wait()

        if verbose:
            sys.stdout.write(f"Successfully tagged {last_block_layer} {tag}\n")


def run():
    main()


if __name__ == "__main__":
    run()
