from __future__ import print_function

import asyncio
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2

SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']
token_file = os.path.join(os.getcwd(), 'token.json')
credentials_file = os.path.join(os.getcwd(), 'credentials.json')

class MeetAPI ():
    def __init__(self):
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_file):
            self.creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(self.creds.to_json())

    async def create_space(self):
        client = meet_v2.SpacesServiceClient(credentials=self.creds)
        request = meet_v2.CreateSpaceRequest()
        response = client.create_space(request=request)
        data = {
            'name': response.name,
            'meeting_uri': response.meeting_uri,
            'meeting_code': response.meeting_code,
            'config': {
                'access_type': response.config.access_type,
                'entry_point_access': response.config.entry_point_access
            }
        }
        return data
    async def get_parent_param(self, meeting_id):
        client = meet_v2.SpacesServiceAsyncClient(credentials=self.creds)
        request = meet_v2.GetSpaceRequest(
            name=f"spaces/{meeting_id}",
        )

        # Make the request
        response = await client.get_space(request=request)
        print(response.name)
        return response.name

        # Handle the response
        # print(response.active_conference.conference_record)
        #
        # return response.active_conference.conference_record

    async def get_name(self, meeting_id):
        client = meet_v2.ConferenceRecordsServiceClient(credentials=self.creds)
        parent = await self.get_parent_param(meeting_id)
        print(parent)
        print("----------------")

        request = meet_v2.ListConferenceRecordsRequest(
        )

        # Make the request
        page_result =  client.list_conference_records(request=request)
        for response in page_result:
            if response.space == parent:
                print(response)
                return response.name


    async def get_participants(self, meeting_id):
        client = meet_v2.ConferenceRecordsServiceAsyncClient(credentials=self.creds)
        parent = await self.get_name(meeting_id)

        request = meet_v2.ListParticipantsRequest(
            parent=parent,
        )

        # Make the request
        page_result = await client.list_participants(request=request)

        # # Handle the response
        participants = []
        async for response in page_result:
            participant = {
                'signedin_user':{
                    'user': response.signedin_user.user,
                    'display_name': response.signedin_user.display_name
                },
                'start_time': response.earliest_start_time,
                'end_time': response.latest_end_time
            }
            participants.append(participant)
        return participants

# if __main__ == "__main__":
#
#
#     meet = MeetAPI()
#     # print(asyncio.run(meet.create_space()))
#     paticipants = asyncio.run(meet.get_participants('nse-rhyz-vac'))
#     for paticipant in paticipants:
#         print(paticipant)
