from core.loader import Loader
from core.game import Story
from core.views import generate_resolve_action_view
from bridge.urls import add_url


def setup():
    """Initialize a basic game structure with
    the local levels installed"""

    levels = Loader.local_levels()
    story = Story()

    for level in levels:
        story.add_level(level)

    add_url(
        "actions/<level_identifier>/<action_identifier>",
        generate_resolve_action_view(story),
    )
