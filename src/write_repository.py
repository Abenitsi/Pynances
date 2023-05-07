import os.path

from datetime import date
import time
from typing import List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.ids import create_id

from src.movements import Movement, Saving, parse_numbers


def get_sheet(scopes):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        return service.spreadsheets()
    except HttpError as err:
        print(err)


def parse_movements_factory(movements):
    insert_movements = []

    if isinstance(movements[0], Movement):
        for m in movements:
            insert_movements.append(m.toList())
    elif isinstance(movements[0], Saving):
        category = ""
        for m in movements:
            if m.category == "Total":
                break
            if m.category != category and m.category != "Sin Asignar":
                category = m.category
                insert_movements.append([category])
            movement = m.toList()
            if m.category == "Sin Asignar":
                movement[0] = "Sin Asignar"
                movement[1] = ""
            insert_movements.append(movement)
    else:
        insert_movements = movements

    return insert_movements


def write_movements(sheet, sheet_id, range_name, movements):
    insert_movements = parse_movements_factory(movements)
    sheet.values().update(
        spreadsheetId=sheet_id,
        valueInputOption="USER_ENTERED",
        range=range_name,
        body={"values": insert_movements},
    ).execute()


def read_movements(sheet, sheet_id, range_name):
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get("values", [])

    if not values:
        print("No data found.")
        return

    movements = []
    for row in values:
        mov_date = date(int(row[6]), int(row[5]), int(row[4]))
        timestamp = time.mktime(mov_date.timetuple())
        movements.append(
            Movement(
                id=row[0],
                comment=row[1],
                description=row[2],
                category=row[3],
                amount=parse_numbers(row[7]),
                day=row[4],
                month=row[5],
                year=row[6],
            )
        )
    return movements


def update_movements(scopes, sheet_id, range_name):
    sheet = get_sheet(scopes)
    movements = read_movements(sheet, sheet_id, range_name)
    write_movements(sheet, sheet_id, range_name, movements)


def get_savings(sheet, sheet_id, range_name):
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get("values", [])
    special_categories = ["Sin Asignar", "Total"]
    category = ""
    savings = []
    for row in values:
        # row[0] not in special_categories
        if category == "" or (row[0] != "" and row[0] != category):
            category = row[0].strip()
            if category not in special_categories:
                continue
        savings.append(
            Saving(
                name=row[1].strip() if row[1].strip() != "" else category,
                category=category,
                goal=parse_numbers(row[3].strip()) if row[3].strip() != "-   €" else 0,
                current=parse_numbers(row[2].strip())
                if row[2].strip() != "-   €"
                else 0,
                income=parse_numbers(row[4].strip())
                if row[4].strip() != "-   €"
                else 0,
            )
        )

    return savings
