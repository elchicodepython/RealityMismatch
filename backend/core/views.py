from django.http import JsonResponse

from .types import LevelIdentifier, ActionIdentifier


def generate_resolve_action_view(story):
    def view_data(request, level_identifier, action_identifier, *args, **kwargs): # bridge
        def action_wrapper(level_identifier: LevelIdentifier, action_identifier: ActionIdentifier):
            return JsonResponse(story.resolve_action(level_identifier, action_identifier).action())
        return action_wrapper(level_identifier, action_identifier)
    return view_data
