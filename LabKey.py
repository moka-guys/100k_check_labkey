#!/usr/bin/env python3
"""
LabKey.py

Query labkey for a participant ID name, date of birth and NHS number.

Example:
    LabKey.py -i <participant_id> [ -u <labkey_username> ] [ -p <labkey_password> ]
>>> 'NAME,DOB,NHSNUM'
"""

import argparse
import datetime
import pprint
import requests
import sys


class LabKey_HTTP():
    """Connect to GEL LabKey API via HTTP and return JSON data for a given PID.

    Args:
        PID: A GEL participant ID
        username: A LabKey user (typically an Email address)
        password: LabKey password for given username
    Attributes:
        data (str): A dictionary containig the json object returned by the LabKey API
        name (str): Participant full name
        dob (str): Participant date of birth in the format: "DAY/MONTH/YEAR"
        nhsid (str): Participant NHS number
    Methods:
        print_data(): Prints self.data to stdout
        print_details(): Prints the patient Name, Date of birth and NHS id to stdout as a comma-separated string
    """
    def __init__(self, PID, username=None, password=None):
        # Set user credentials
        self.PID = PID
        self.uname = username
        self.pwd = password

        # Get json data from LabKey API
        self.data = self.get_data()
        self.PID_data = self.data['rows'][0]

        # Set the following patient details as object attributes: Name, Date of Birth, NHS number
        self.name = self.PID_data['forenames'] + ' ' + self.PID_data['surname']
        self.raw_dob = self.PID_data['date_of_birth']
        self.nhsid = self.PID_data['person_identifier']
        # Clean date of birth to format: "DAY/MONTH/YEAR"
        self.date = datetime.datetime.strptime(self.raw_dob, '%Y/%m/%d %H:%M:%S').date()
        self.dob = self.date.strftime('%d/%m/%Y')

    def get_data(self):
        '''Pull JSON data from LabKey API for input participant ID.

        Returns:
            response_json (dict): LabKey API response json as dict
        '''
        # Set URL for LabkeyAPI
        URL = ("https://gmc.genomicsengland.nhs.uk/labkey/query/Genomics England Portal/"
            "South London/MeRCURy/Rare Diseases/Core/selectRows.api")
        # Define payload. query.columns filters data for PID.
        # Columns returned are: 
        # participant_id = GeL participant ID
        # person_identifier = NHS number
        # date_of_birth = date of birth
        # forenames = Forenames
        # surname = Surname
        # person_identifier_type = A text description of the person identifier (nhsNumber)
        payload = {'schemaName': 'gel_rare_diseases', 'query.queryName': 'participant_identifier', 
            'query.columns': 'participant_id,person_identifier,date_of_birth,forenames,surname,person_identifier_type',
            'query.participant_id~eq': self.PID}
        # Make API call with auth credentials if provided.
        if self.uname or self.pwd:
            response_json = requests.get(URL, params=payload, auth=(self.uname, self.pwd)).json()
        else:
            response_json = requests.get(URL, params=payload).json()

        # Raise error if more or less than one participant is matched by the PID. This is because PIDs are unique.
        if response_json['rowCount'] != 1:
            raise IndexError('More/less than one row returned for participant ID {}'.format(self.PID))
        return(response_json)
    
    def print_data(self):
        print(self.data, end="")

    def print_details(self):
        print(",".join([self.name, self.dob, self.nhsid]), end="")

def main():
    # Parse PID from arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--pid', required=True, help="A Genomics England participant ID")
    parser.add_argument('-u', '--username', help="A Genomics England LabKey username")
    parser.add_argument('-p', '--password', help="A Genomics England LabKey password")
    parsed_args = parser.parse_args()

    # Call LabKey_HTTP() with Participant ID
    if parsed_args.username or parsed_args.password:
        lk_obj = LabKey_HTTP(parsed_args.pid, parsed_args.username, parsed_args.password)
    else:
        lk_obj = LabKey_HTTP(parsed_args.pid)

    # Print JSON result to console
    lk_obj.print_details()

if __name__ == "__main__":
    main()