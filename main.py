from typing import List
from src.movements import Movement
from src.retrieve_repository import (
    AccountType,
    get_account_id,
    get_movements_factory,
    get_movements_factory,
    get_seet,
)
from config import accounts
from src.write_repository import (
    get_savings,
    read_movements,
    get_sheet as get_drive_sheet,
    update_movements,
    write_movements,
)


def categorize(movement: Movement, movements: List[Movement]) -> Movement:
    possible_categories = {}
    for m in movements:
        if m.category and m.description == movement.description:
            if m.category not in possible_categories:
                possible_categories[m.category] = 0
            possible_categories[m.category] += 1
    possible_categories = sorted(
        possible_categories.items(), key=lambda x: x[1], reverse=True
    )
    if len(possible_categories) > 0:
        movement.category = possible_categories[0][0]

    return movement


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


import os
import re

rootdir = "/Users/albert/Projects/Pynances/data"
regex = re.compile("Movements.*")
bank_files = []
for root, dirs, files in os.walk(rootdir):
    for file in files:
        file = file.replace(".xlsx", "").replace(".xls", "")
        if regex.match(file) and file not in bank_files:
            bank_files.append(f"data/{file}")

for file in list(set(bank_files)):
    sheet = get_seet(file)
    drive_sheet = get_drive_sheet(SCOPES)
    account_id = get_account_id(sheet)

    new_movements = get_movements_factory(accounts[account_id]["type"], sheet)
    movements = read_movements(
        drive_sheet,
        accounts[account_id]["spreadsheet"],
        accounts[account_id]["range"],
    )

    last_movement = movements[0]
    movements_to_insert = []
    for m in new_movements:
        if m.id == last_movement.id:
            break
        m = categorize(m, movements)
        movements_to_insert.append(m)

    if accounts[account_id]["type"] is AccountType.SAVING:
        savings = get_savings(
            drive_sheet,
            accounts[account_id]["spreadsheet"],
            accounts[account_id]["saving_range"],
        )
        negative_movements = []
        for m in movements_to_insert:
            total = m.amount
            if total < 0:
                negative_movements.append([m.date(), m.amount, m.description])

            for s in savings:
                if s.goal == s.current:
                    continue

                if total <= 0:
                    break

                if s.category == "Sin Asignar":
                    income = total
                else:
                    if (s.goal - s.current) >= s.income:
                        income = s.income if total >= s.income else total
                    else:
                        income = s.goal - s.current

                total -= income
                s.current += income

        if len(savings) > 0:
            write_movements(
                drive_sheet,
                accounts[account_id]["spreadsheet"],
                accounts[account_id]["saving_range"],
                savings,
            )
        if len(negative_movements) > 0:
            write_movements(
                drive_sheet,
                accounts[account_id]["spreadsheet"],
                accounts[account_id]["negative_saving_range"],
                negative_movements,
            )
    movements_to_insert.extend(movements)
    write_movements(
        drive_sheet,
        accounts[account_id]["spreadsheet"],
        accounts[account_id]["range"],
        movements_to_insert,
    )
