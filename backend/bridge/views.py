from django.http import JsonResponse

from core.types import LevelIdentifier, ActionIdentifier


def action_view(
    story,
    # If I import Story type from game this makes a circular
    # reference so I don't know how to specify Story type without
    # importing it and as it only has only effect in type checking
    # by mypy i will leave without specifying its type right now.
    level_identifier: LevelIdentifier,
    action_identifier: ActionIdentifier,
):
    return JsonResponse(
        story.resolve_action(level_identifier, action_identifier).action()
    )
