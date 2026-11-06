
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .routing import route_between


@require_GET
def route_api(request):

    try:
        start_lat = float(request.GET["start_lat"])
        start_lon = float(request.GET["start_lon"])

        goal_lat = float(request.GET["goal_lat"])
        goal_lon = float(request.GET["goal_lon"])

        algorithm = request.GET.get("algorithm", "astar")

        result = route_between(
            start_lat,
            start_lon,
            goal_lat,
            goal_lon,
            algorithm
        )

        status = 200 if result["success"] else 404

        return JsonResponse(result, status=status)

    except KeyError as error:
        return JsonResponse({
            "success": False,
            "error": f"Missing parameter: {error.args[0]}"
        }, status=400)

    except (ValueError, TypeError) as error:
        return JsonResponse({
            "success": False,
            "error": str(error)
        }, status=400)
from django.shortcuts import render


def map_page(request):
    return render(request, "mapengine/index.html")

