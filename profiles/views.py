import json
import uuid6
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from .models import Profile
from .utils import fetch_external_data

def api_docs(request):
    """Render the API documentation page"""
    return render(request, 'docs.html')

def add_cors(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


def error_response(status, message):
    res = JsonResponse({'status': 'error', 'message': message}, status=status)
    return add_cors(res)


def json_response(data, status=200):
    res = JsonResponse(data, status=status)
    return add_cors(res)


@method_decorator(csrf_exempt, name='dispatch')
class ProfileListCreateView(View):

    def options(self, request, *args, **kwargs):
        res = HttpResponse(status=204)
        res['Access-Control-Allow-Origin'] = '*'
        res['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, OPTIONS'
        res['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return res

    def post(self, request):
        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return error_response(400, 'Invalid JSON body')

        # Check type first — if name key exists but is not a string
        name_raw = body.get('name')

        if name_raw is None or name_raw == '':
            return error_response(400, 'Missing or empty name')

        if not isinstance(name_raw, str):
            return error_response(422, 'Invalid type')

        name = name_raw.strip()

        if not name:
            return error_response(400, 'Missing or empty name')

        # Idempotency check
        try:
            existing = Profile.objects.get(name__iexact=name)
            return json_response({
                'status': 'success',
                'message': 'Profile already exists',
                'data': existing.to_dict(full=True),
            }, status=200)
        except Profile.DoesNotExist:
            pass

        # Fetch from external APIs
        try:
            data = fetch_external_data(name)
        except ValueError as e:
            return error_response(502, str(e))

        profile_id = str(uuid6.uuid7())

        profile = Profile.objects.create(
            id=profile_id,
            name=name.lower(),
            **data,
        )

        return json_response({'status': 'success', 'data': profile.to_dict(full=True)}, status=201)

    def get(self, request):
        queryset = Profile.objects.all()

        gender = request.GET.get('gender', '').strip().lower()
        country_id = request.GET.get('country_id', '').strip().upper()
        age_group = request.GET.get('age_group', '').strip().lower()

        if gender:
            queryset = queryset.filter(gender__iexact=gender)
        if country_id:
            queryset = queryset.filter(country_id__iexact=country_id)
        if age_group:
            queryset = queryset.filter(age_group__iexact=age_group)

        profiles = [p.to_dict(full=False) for p in queryset]
        return json_response({'status': 'success', 'count': len(profiles), 'data': profiles}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class ProfileDetailView(View):

    def options(self, request, *args, **kwargs):
        res = HttpResponse(status=204)
        res['Access-Control-Allow-Origin'] = '*'
        res['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, OPTIONS'
        res['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return res

    def get(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            return error_response(404, 'Profile not found')

        return json_response({'status': 'success', 'data': profile.to_dict(full=True)}, status=200)

    def delete(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            return error_response(404, 'Profile not found')

        profile.delete()
        res = HttpResponse(status=204)
        res['Access-Control-Allow-Origin'] = '*'
        return res