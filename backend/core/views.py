from bridge.views import action_view
from .types import LevelIdentifier, ActionIdentifier


def generate_resolve_action_view(story):
    def view_data(
        request,
        level_identifier: LevelIdentifier,
        action_identifier: ActionIdentifier,
        *args,
        **kwargs
    ):
        return action_view(story, level_identifier, action_identifier)

    return view_data
