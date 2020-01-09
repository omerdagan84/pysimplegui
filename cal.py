#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_events():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    ev_list = dict()
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    calendars = service.calendarList().list().execute()
    print(type(calendars))
    cal_list = []
    for x in calendars['items']:
        cal_list.append(x['id'])
    print(cal_list)
#    print(calendars['items'][]['id'])
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    for i in cal_list:
        print('Getting the upcoming 10 events from "{0}"'.format(i))
        events_result = service.events().list(calendarId=i, timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            if any("\u0590" <= c <= "\u05EA" for c in event['summary']):
                ev_list[event['start'].get('dateTime', event['start'].get('date'))] = event['summary'][::-1]
            else:
                ev_list[event['start'].get('dateTime', event['start'].get('date'))] = event['summary']

    print(ev_list)
    return ev_list
if __name__ == '__main__':
    get_events()
