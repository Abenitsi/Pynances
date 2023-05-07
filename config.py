from src.retrieve_repository import AccountType

privada_spreadsheet = "11d4c35d666hS9c7awyxkSZ-H1bCgfTCGyli87YKqBWo"
comuna_spreadsheet = "1rwSkcRFCB_aIBdn8HpzFUPrRtk-mNQoJWBwX4ogGijM"
accounts = {
    "1f97570c89c54806a62adee456b57e9c47d2dac69c387d0041ecf2ac783cf53b": {
        "spreadsheet": privada_spreadsheet,
        "range": "Cuenta NÓMINA Privada!A2:H",
        "type": AccountType.REGULAR,
    },
    "262f24ea28bba1383d679dca6638197b076806133fc3d30349c24b5a38b8d02a": {
        "spreadsheet": comuna_spreadsheet,
        "range": "Cuenta NÓMINA Comuna!A2:H",
        "type": AccountType.REGULAR,
    },
    "a877de8b8379173d04886f65852497a937786c91af90283d4c6ef6c26c7d33b4": {
        "spreadsheet": privada_spreadsheet,
        "range": "Cuenta NARANJA Privada!A2:H",
        "saving_range": "Huchas!A3:E",
        "negative_saving_range": "Huchas!H2:J",
        "type": AccountType.SAVING,
    },
    "772a3da3094fe3be3ed3f468f45903a9441db9fb10c6fb96182249476e937f0b": {
        "spreadsheet": comuna_spreadsheet,
        "range": "Cuenta NARANJA Comuna!A2:H",
        "saving_range": "Huchas!A3:E",
        "negative_saving_range": "Huchas!H2:J",
        "type": AccountType.SAVING,
    },
    "dc937b59892604f5a86ac96936cd7ff09e25f18ae6b758e8014a24c7fa039e91": {
        "spreadsheet": privada_spreadsheet,
        "range": "Tarjeta Crédito!A2:H",
        "type": AccountType.CREDIT_CARD,
    },
    # "08df0748a71f6b825876322db3aa3ebb2d62b8352a0bb02ec40286d425d32162": {
    #     "spreadsheet": "",
    #     "range": "",
    #     "type": AccountType.INVESTMENT
    # }
}
