from __future__ import print_function

import asyncio
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']


async def main():
    """Shows basic usage of the Google Meet API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # client = meet_v2.SpacesServiceClient(credentials=creds)
        # request = meet_v2.CreateSpaceRequest()
        # response = client.create_space(request=request)
        # print(f'Space created: {response}')
        client = meet_v2.SpacesServiceAsyncClient(credentials=creds)

        # Initialize request argument(s)
        request = meet_v2.GetSpaceRequest(
            name="spaces/ruj-gnuj-ehm",
        )

        # Make the request
        response = await client.get_space(request=request)

        # Handle the response
        print(response)

        # Create a client
        # client = meet_v2.ConferenceRecordsServiceAsyncClient(credentials=creds)
        #
        # # Initialize request argument(s)
        # request = meet_v2.GetConferenceRecordRequest(
        #     name="spaces/dte-xjdh-qmq",
        # )
        #
        # # Make the request
        # response = await client.get_conference_record(request=request)
        #
        # # Handle the response
        # print(response)

        # client = meet_v2.ConferenceRecordsServiceAsyncClient(credentials=creds)
        #
        # # Initialize request argument(s)
        # request = meet_v2.ListParticipantsRequest(
        #     parent="conferenceRecords/279f294e-20c9-4f54-8d05-658f76c9332e",
        # )
        #
        # # Make the request
        # page_result = await client.list_participants(request=request)
        #
        # # Handle the response
        # async for response in page_result:
        #     print(response)
    except Exception as error:
        # TODO(developer) - Handle errors from Meet API.
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    asyncio.run(main())