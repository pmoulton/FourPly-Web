from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import util
import json


@csrf_exempt
def new_user(request):
    if request.method == "GET":
        return HttpResponse(status=400)

    username = request.POST['username']
    token = request.POST['token']
    new_user = None

    try:
        new_user = User.objects.create_user(username, "", token)
        user1 = UserProfile(user=new_user)
    except Exception as e:
        if new_user:
            new_user.delete()
        response_data = {'error': "username already exists"}
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=400)

    user1.user_uid = str(uuid.uuid4())
    user1.save()
    response_data = {'error': "none", 'username': username}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def new_bathroom(request):
    if request.method == "GET":
        return util.bad_request("GET not allowed")
    user_profile = util.auth_user(request)
    if not user_profile:
        return util.auth_failed()
    try:
        lat, lon, has_twoply, name = util.get_post_args(request, ("lat", "lon", "has_twoply", "name"))
    except KeyError:
        return util.bad_request("invalid args")
    if not user_profile:
        return util.auth_failed()
    bathroom = Bathroom(name=name, lat=lat, lon=lon, has_twoply=has_twoply, uid=str(uuid.uuid4()))
    bathroom.save()
    response_data = {'error': "none", 'id': bathroom.uid}
    return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)


def upload_photo(request):
    return HttpResponse(status=400)


def check_in(request):
    return

@csrf_exempt
def add_rating(request):
    if request.method == "GET":
        return util.bad_request("GET not allowed")
    user_profile = util.auth_user(request)
    if not user_profile:
        return util.auth_failed()
    try:
        u_id = util.get_post_args(request, ["uid"])
        rating = util.get_post_args(request, ["rating"])
    except KeyError:
        return util.bad_request("Invalid args")
    try:
        bathroom = Bathroom.objects.get(uid=u_id)
    except ObjectDoesNotExist as e:
        return util.bad_request("bathroom not found")
    if user_profile.ratings.filter(uid=u_id) > 0:
        bathroom.num_hearts -= 1
    else:
        user_profile.ratings.add(bathroom)
        bathroom.num_ratings += 1
        bathroom.total_rating += rating
        bathroom.rating = bathroom.total_rating/(5*bathroom.num_ratings)

@csrf_exempt
def heart_bathroom(request):
    if request.method == "GET":
        return util.bad_request("GET not allowed")
    user_profile = util.auth_user(request)
    if not user_profile:
        return util.auth_failed()
    try:
        u_id = util.get_post_args(request, ["uid"])
    except KeyError:
        return util.bad_request("Invalid args")
    try:
        bathroom = Bathroom.objects.get(uid=u_id)
    except ObjectDoesNotExist as e:
        return util.bad_request("bathroom not found")
    if user_profile.hearts.filter(uid=u_id) > 0:
        bathroom.num_hearts -= 1
    else:
        user_profile.hearts.add(bathroom)
        bathroom.num_hearts += 1


def like_review(request):
    return HttpResponse(status=400)


def get_nearby_bathrooms(request):
    if request.method == "GET":
        return HttpResponse(status=400)
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']



