"""Root module for sphinx-revealjs."""

__version__ = "1.0.1"


from sphinx.application import Sphinx

from sphinx_revealjs.builders import RevealjsHTMLBuilder
from sphinx_revealjs.directives import (
    RevealjsBreak,
    RevealjsFragments,
    RevealjsSection,
    RevealjsSlide,
)
from sphinx_revealjs.nodes import (
    revealjs_break,
    revealjs_fragments,
    revealjs_section,
    revealjs_slide,
)
from sphinx_revealjs.themes import get_theme_path
from sphinx_revealjs.writers import (
    depart_revealjs_break,
    not_write,
    visit_revealjs_break,
)


def setup(app: Sphinx):
    """Set up function called by Sphinx."""
    app.add_builder(RevealjsHTMLBuilder)
    app.add_node(
        revealjs_section, html=(not_write, not_write), revealjs=(not_write, not_write)
    )
    app.add_node(
        revealjs_break,
        html=(not_write, not_write),
        revealjs=(visit_revealjs_break, depart_revealjs_break),
    )
    app.add_node(
        revealjs_slide, html=(not_write, not_write), revealjs=(not_write, not_write)
    )
    app.add_node(
        revealjs_fragments, html=(not_write, not_write), revealjs=(not_write, not_write)
    )
    app.add_directive("revealjs_break", RevealjsBreak)
    app.add_directive("revealjs_section", RevealjsSection)
    app.add_directive("revealjs_slide", RevealjsSlide)
    app.add_directive("revealjs_fragments", RevealjsFragments)
    app.add_config_value("revealjs_static_path", [], True)
    app.add_config_value("revealjs_style_theme", "black", True)
    app.add_config_value("revealjs_css_files", [], True)
    app.add_config_value("revealjs_google_fonts", [], True)
    app.add_config_value("revealjs_generic_font", "sans-serif", True)
    app.add_config_value("revealjs_script_files", [], True)
    app.add_config_value("revealjs_script_conf", None, True)
    app.add_config_value("revealjs_script_plugins", [], True)
    app.add_html_theme("sphinx_revealjs", str(get_theme_path("sphinx_revealjs")))
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": False,
    }
