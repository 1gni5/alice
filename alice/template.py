from importlib import import_module
from pathlib import Path

from jinja2 import FileSystemLoader, Environment

def build_context(metadata: dict) -> dict:
    """Build the context for template rendering."""

    context = dict()
    plugins = metadata.get('plugins', {})

    # Get context for every installed plugin
    for name, args in plugins.items():
        module = import_module(f"alice.plugins.{name}")
        context |= module.context_builder(**args)

    return context

def render(filename: str, context: dict) -> str:
    """Fill-in script template with given context."""

    environment = Environment(loader=FileSystemLoader("templates"))
    template = environment.get_template(filename)

    return template.render(**context)