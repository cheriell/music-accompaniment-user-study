from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer

from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from .models import UserStudyRating, RatingValue

max_user_number = 30

def index(request):
    user_study_ratings = UserStudyRating.objects.all()
    status_on = True
    count = 0
    for user_study_rating in user_study_ratings:
        count += 1
    if count > max_user_number:
        status_on = False
    context = {
        'status_on': status_on,
    }
    return render(request, 'index.html', context)

def consent_form(request):
    user_study_ratings = UserStudyRating.objects.all()
    status_on = True
    count = 0
    for user_study_rating in user_study_ratings:
        count += 1
    if count > max_user_number:
        status_on = False
    context = {
        'status_on': status_on,
    }
    return render(request, 'consent_form.html', context)

def user_study(request):
    user_study_ratings = UserStudyRating.objects.all()
    status_on = True
    count = 0
    for user_study_rating in user_study_ratings:
        count += 1
    if count > max_user_number:
        status_on = False
    rating_values = RatingValue.objects.all()
    context = {
        'status_on': status_on,
        'rating_values': rating_values,
        'segments': [
            {'no': '1', 'name': 'mond_2_segment1', 'left': 'true' },
            {'no': '2', 'name': 'chp_op18_segment1', 'left': 'false'},
            {'no': '3', 'name': 'viennese1-4_segment1', 'left': 'true' },
            {'no': '4', 'name': 'tmte04-63j_segment1', 'left': 'false'},
            {'no': '5', 'name': 'clementi_opus36_5_3_segment1', 'left': 'true' },
        ],
        'suffixes': [
            {'no': '1', 'value': 'chroma-beat' },
            {'no': '2', 'value': 'chroma-mode' },
            {'no': '3', 'value': 'midi-pitch' },
            {'no': '4', 'value': 'chroma-based' },
            {'no': '5', 'value': 'chroma-pure' },
        ],
        'music_styles': [
            {'value': 'African'},
            {'value': 'Arabic Music'},
            {'value': 'Asian'},
            {'value': 'Blues'},
            {'value': 'Country'},
            {'value': 'Electronic Music'},
            {'value': 'Folk'},
            {'value': 'Hip Hop'},
            {'value': 'Jazz'},
            {'value': 'Latin'},
            {'value': 'Pop'},
            {'value': 'Rock'},
            {'value': 'Western Classical Music'},
            {'value': 'Other'},
        ],
    }
    return render(request, 'user_study.html', context)

def thanks(request):
    # create user_study_rating object
    rating1_1 = request.POST['rating1_1']
    rating1_2 = request.POST['rating1_2']
    rating1_3 = request.POST['rating1_3']
    rating1_4 = request.POST['rating1_4']
    rating1_5 = request.POST['rating1_5']

    rating2_1 = request.POST['rating2_1']
    rating2_2 = request.POST['rating2_2']
    rating2_3 = request.POST['rating2_3']
    rating2_4 = request.POST['rating2_4']
    rating2_5 = request.POST['rating2_5']

    rating3_1 = request.POST['rating3_1']
    rating3_2 = request.POST['rating3_2']
    rating3_3 = request.POST['rating3_3']
    rating3_4 = request.POST['rating3_4']
    rating3_5 = request.POST['rating3_5']

    rating4_1 = request.POST['rating4_1']
    rating4_2 = request.POST['rating4_2']
    rating4_3 = request.POST['rating4_3']
    rating4_4 = request.POST['rating4_4']
    rating4_5 = request.POST['rating4_5']

    rating5_1 = request.POST['rating5_1']
    rating5_2 = request.POST['rating5_2']
    rating5_3 = request.POST['rating5_3']
    rating5_4 = request.POST['rating5_4']
    rating5_5 = request.POST['rating5_5']

    general_a = request.POST['general_a']
    general_b = request.POST['general_b']
    general_c = request.POST['general_c']

    years_musical_training = request.POST['years_musical_training']
    music_style = request.POST['music_style']
    name = request.POST['name']

    user_study_rating = UserStudyRating(rating1_1=rating1_1, rating1_2=rating1_2, rating1_3=rating1_3, rating1_4=rating1_4, rating1_5=rating1_5, rating2_1=rating2_1, rating2_2=rating2_2, rating2_3=rating2_3, rating2_4=rating2_4, rating2_5=rating2_5, rating3_1=rating3_1, rating3_2=rating3_2, rating3_3=rating3_3, rating3_4=rating3_4, rating3_5=rating3_5, rating4_1=rating4_1, rating4_2=rating4_2, rating4_3=rating4_3, rating4_4=rating4_4, rating4_5=rating4_5, rating5_1=rating5_1, rating5_2=rating5_2, rating5_3=rating5_3, rating5_4=rating5_4, rating5_5=rating5_5, general_a=general_a, general_b=general_b, general_c=general_c, years_musical_training=years_musical_training, music_style=music_style, name=name)

    # set serial number and save user_study_rating
    user_study_ratings = UserStudyRating.objects.all()

    last_rating = UserStudyRating()
    new_rating = True
    last_serial_no = 0
    for r in user_study_ratings:
        last_serial_no = r.serial_no
        if serialise(user_study_rating) == serialise(r):
            new_rating = False
            user_study_rating.serial_no = r.serial_no
    if new_rating:
        user_study_rating.serial_no = last_serial_no + 1
        user_study_rating.save()

    # prize
    prize = False
    if user_study_rating.serial_no % 5 == 0:
        prize = True
    
    context = {
        'name': name,
        'serial_no': user_study_rating.serial_no,
        'prize': prize,
    }
    return render(request, 'thanks.html', context)

def thanks2(request):
    serial_no = request.POST['serial_no']
    email = request.POST['email']
    note = request.POST['note']

    user_study_rating = UserStudyRating.objects.get(serial_no=serial_no)
    user_study_rating.email = email
    user_study_rating.note = note
    user_study_rating.save()

    context = {
        'name': user_study_rating.name,
        'serial_no': serial_no,
        'email': email,
        'note': note,
    }
    return render(request, 'thanks2.html', context)


def serialise(r):
    # serialise an UserStudyRating's information except for its seiral_no
    result = ''
    result += str(r.rating1_1) + str(r.rating1_2) + str(r.rating1_3) + str(r.rating1_4) + str(r.rating1_5)
    result += str(r.rating2_1) + str(r.rating2_2) + str(r.rating2_3) + str(r.rating2_4) + str(r.rating2_5)
    result += str(r.rating3_1) + str(r.rating3_2) + str(r.rating3_3) + str(r.rating3_4) + str(r.rating3_5)
    result += str(r.rating4_1) + str(r.rating4_2) + str(r.rating4_3) + str(r.rating4_4) + str(r.rating4_5)
    result += str(r.rating5_1) + str(r.rating5_2) + str(r.rating5_3) + str(r.rating5_4) + str(r.rating5_5)

    result += r.general_a + r.general_b + r.general_c

    result += r.years_musical_training
    result += r.music_style
    result += r.name

    return result

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer