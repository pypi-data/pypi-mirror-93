import re


def make_block_pattern():
    return re.compile(r"^(Step \d+/\d+ : FROM [^\n]+)$\n", re.MULTILINE | re.IGNORECASE)


def make_block_name_pattern():
    step = r"\d+"
    step_current = fr"(?P<step_current>{step})"
    step_max = fr"(?P<step_max>{step})"
    image = r"[\w$-]+"
    image_base = fr"(?P<image_base>{image})"
    image_target = fr"(?P<image_target>{image})"
    return re.compile(
        fr"Step {step_current}/{step_max} : FROM {image_base} AS {image_target}",
        re.IGNORECASE,
    )


def make_block_tag_pattern():
    layer = r"(?P<layer>\w+)"
    return re.compile(fr" ---> {layer}", re.IGNORECASE)
