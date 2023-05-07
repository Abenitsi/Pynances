from dataclasses import dataclass
import json


@dataclass
class Movement:
    id: str
    comment: str
    description: str
    category: str
    amount: float
    day: int
    month: int
    year: int

    def __init(
        self,
        id: str = "",
        comment: str = "",
        description: str = "",
        category: str = "",
        amount: float = "",
        day: int = 1,
        month: int = 1,
        year: int = 1970,
    ):
        self.id = id
        self.comment = comment
        self.description = description
        self.category = category
        self.amount = amount
        self.day = day
        self.month = month
        self.year = year

    def date(self):
        return f"{str(self.day).rjust(2, '0')}/{str(self.month).rjust(2, '0')}/{str(self.year)}"

    def toList(self):
        return [
            self.id,
            self.description,
            self.comment,
            self.category,
            str(self.day).rjust(2, "0"),
            str(self.month).rjust(2, "0"),
            str(self.year),
            self.amount,
        ]


def parse_numbers(number: str):
    number = number.replace(" €", "")
    number = number.replace(" ", "")
    number = number.replace(".", "")
    number = number.replace(",", ".")

    return float(number)


@dataclass
class Saving:
    name: str
    category: str
    goal: float
    current: float
    income: float

    @property
    def months(self) -> int:
        return int((self.goal - self.current) / self.income)

    def toList(self):
        return ["", self.name, self.current, self.goal, self.income]
