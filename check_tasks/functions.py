from string import Template

from .config import config


def read_template():
    with open(config.TEMPLATE_EMAIL, 'r', encoding='utf-8') as f:
        content = f.read()
    return Template(content)
