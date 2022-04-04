Se overgang.py, forsøk å forstå
NB: bundla skjema er for 2020


Eksempel med output:
>python overgang.py database.csv
building pdf for:
{'overgang': 'ja', 'gammelklubb': 'Gamleklubben', 'id': '123', 'kjonn': 'Male', 'fornavn': 'Ola', 'fodselsdato': '01.01.1970', 'etternavn': 'Nordmann', 'phoneNumber': '12345678', 'adresse': 'Gategata 123', 'postnr': '1', 'epost': 'epost@epost.epost', 'kortnr': 'XXXXX', 'kommentar': '', 'regdato': 'XX.XX.XXXX', 'kontrolldato': 'XX.XX.XXXX', 'gammelKlubb': '', 'ekstra': 'NULL', 'harUtførtFrivilligArbeid': 'NULL', 'triatlon': '0'}
{'name': 'Ola Nordmann', 'birth': '01.01.1970', 'addr': 'Gategata 123', 'post': '0001', 'sted': 'OSLO', 'prev': 'Gamleklubben', 'new': 'NTNUI-Svømming', 'X': 'X'}
Using template overgangsskjema2020.pdf
Writing to Ola Nordmann.pdf
Done

building pdf for:
{'overgang': 'nei', 'gammelklubb': 'klubb2', 'id': '124', 'kjonn': 'Female', 'fornavn': 'Kari', 'fodselsdato': '01.01.2970', 'etternavn': 'Nordmann', 'phoneNumber': '98765432', 'adresse': 'Gategate 321', 'postnr': '7025', 'epost': 'epost2@epost.epost', 'kortnr': 'XXXXX', 'kommentar': '', 'regdato': 'XX.XX.XXXX', 'kontrolldato': 'XX.XX.XXXX', 'gammelKlubb': '', 'ekstra': 'NULL', 'harUtførtFrivilligArbeid': 'NULL', 'triatlon': '0'}
{'name': 'Kari Nordmann', 'birth': '01.01.2970', 'addr': 'Gategate 321', 'post': '7025', 'sted': 'TRONDHEIM', 'prev': 'klubb2', 'new': 'NTNUI-Svømming', 'X': 'X'}
Using template EndringAvKlubbtilhorighet2020.pdf
Writing to Kari Nordmann.pdf
Done