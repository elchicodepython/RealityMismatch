from django.http import JsonResponse

from sdk.level import LevelView


def get_view(level_view: LevelView):
    def view_wrapper(request, *args, **kwargs):
        response = level_view.action(request, *args, **kwargs)
        return JsonResponse(response)

    return view_wrapper
