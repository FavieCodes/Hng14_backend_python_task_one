import uuid
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Profile
from .utils import fetch_external_data
from django.shortcuts import render

def api_docs(request):
    return render(request, 'docs.html')


def error_response(status, message):
    return JsonResponse({'status': 'error', 'message': message}, status=status)


@method_decorator(csrf_exempt, name='dispatch')
class ProfileListCreateView(View):

    def post(self, request):
        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return error_response(400, 'Invalid JSON body')

        name = body.get('name', '').strip()

        if not name:
            return error_response(400, 'Missing or empty name')

        if not isinstance(name, str):
            return error_response(422, 'Invalid type')

        # Idempotency check — return existing profile if name already stored
        try:
            existing = Profile.objects.get(name__iexact=name)
            return JsonResponse({
                'status': 'success',
                'message': 'Profile already exists',
                'data': existing.to_dict(full=True),
            }, status=200)
        except Profile.DoesNotExist:
            pass

        # Fetch data from external APIs
        try:
            data = fetch_external_data(name)
        except ValueError as e:
            return error_response(502, str(e))

        # Generate UUID v7
        profile_id = str(uuid.uuid7())

        profile = Profile.objects.create(
            id=profile_id,
            name=name.lower(),
            **data,
        )

        return JsonResponse({'status': 'success', 'data': profile.to_dict(full=True)}, status=201)

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
        return JsonResponse({'status': 'success', 'count': len(profiles), 'data': profiles}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class ProfileDetailView(View):

    def get(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            return error_response(404, 'Profile not found')

        return JsonResponse({'status': 'success', 'data': profile.to_dict(full=True)}, status=200)

    def delete(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            return error_response(404, 'Profile not found')

        profile.delete()
        return HttpResponse(status=204)