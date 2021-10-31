from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from datetime import datetime
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.db import transaction
from django.shortcuts import render

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def collector(request):
    if request.method == 'POST':

        # Query all sessions
        eye_sessions = Session.objects.all()

        # Initialize flag variable
        # flag=False if session with session_id not exist else flag=True
        flag = False
        s_key = ''

        # Search if session with key:session_id exist
        for s in eye_sessions:
            events_dict = s.get_decoded()

            # if session exist then flag = True and store session_key to s_key variable
            if events_dict.get(request.data['session_id']) is not None:
                flag = True
                s_key = s.session_key
                break

        # controlling the database transactions using atomic
        with transaction.atomic():

            # if flag=True then update session value else create new session with
            if flag:

                # Find session which will be updated
                s = SessionStore(session_key=s_key)
                # Convert json to dict
                events_list = json.loads(s[request.data['session_id']])

                # Insert event in session events list with descending order comparing timestamp
                pos = 0
                for l in events_list:
                    if datetime.strptime(request.data['timestamp'],'%Y-%m-%d %H:%M:%S.%f') > datetime.strptime(l['timestamp'],'%Y-%m-%d %H:%M:%S.%f'):
                        break
                    pos = pos + 1

                events_list.insert(pos,request.data)

                #Convert dict to json
                events_json = json.dumps(events_list)

                # Update session value
                s[request.data['session_id']] = events_json
                s.save()

                return Response('Session with session_id:'+ request.data['session_id'] +' updated!')

            else:

                #Events list is epmty
                #Add new event to events_list
                events_list = []
                events_list.append(request.data)

                #Create new Session with key = session_key
                new_session = SessionStore()
                new_session[request.data['session_id']] = json.dumps(events_list)
                new_session.create()

                return Response('Session with session_id:'+ request.data['session_id'] +' added!')

    return Response('Not allowed Method')




############################
# Query events from Sessions
############################


# Return specific session by session_id
def getSession(request):

    event = ''
    eye_sessions = Session.objects.all()

    for s in eye_sessions:
        events_dict = s.get_decoded()
        if events_dict.get('e2085be5-9137-4e4e-80b5-f1ffddc25423') is not None:
            event = events_dict.values()
            break

    context = {'event':event}
    return render(request,'eye/event.html',context)


# Return events by specific category. Example category == page interaction
def catEvents(request):

    events_list = []
    eye_sessions = Session.objects.all()

    for s in eye_sessions:
        for values in s.get_decoded().values():
            for v in json.loads(values):
                if 'category' in v.keys():
                    if v['category'] == 'page interaction':
                        events_list.append(v)

    context = {'events_list':events_list}
    return render(request,'eye/catEvents.html',context)


# Return events between time range
def timeRangeEvents(request):

    events_list = []
    eye_sessions = Session.objects.all()

    for s in eye_sessions:
        for values in s.get_decoded().values():
            for v in json.loads(values):
                if 'timestamp' in v.keys():
                    e_time = datetime.strptime(v['timestamp'],'%Y-%m-%d %H:%M:%S.%f')
                    if (e_time >= datetime.strptime('2020-01-01 09:15:27.243860','%Y-%m-%d %H:%M:%S.%f')) and (e_time <= datetime.strptime('2021-01-01 09:15:27.243860','%Y-%m-%d %H:%M:%S.%f')):
                        events_list.append(v)

    context = {'events_list':events_list}
    return render(request,'eye/timeRangeEvents.html',context)


# Return events with invalid timestamp
def invalidTimestamp(request):

    events_list = []
    eye_sessions = Session.objects.all()

    for s in eye_sessions:
        for values in s.get_decoded().values():
            for v in json.loads(values):
                if 'timestamp' in v.keys():
                    e_time = datetime.strptime(v['timestamp'],'%Y-%m-%d %H:%M:%S.%f')
                    if e_time > datetime.now():
                        events_list.append(v)

    context = {'events_list':events_list}
    return render(request,'eye/invalidTimestamp.html',context)


