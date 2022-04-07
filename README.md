# Swimming transfer form generator

Auto generate transfer forms ("Overgangsskjema") and association transfer forms ("Endring av klubbtilhørighet") for new members.

Whenever new athletes tries to join a new swimming group they will need to transfer their club association. This is necessary because only one club at a time can generate payment information for the swimming license. And without the license the athlete might not compete in official events or attend practices. Unfortunately, this process cannot be fully automated because signature of the athlete is required. However board member responsible for filling out the form will have much less work.

For some unknown reason there are two forms. If the athlete have had an active membership the past two years then "Overgangsskjema" needs to be used. Otherwise the "Endring av klubbtilhørighet" has to be used. The form needs to be sent to the athlete after it has been generated. The athlete will then have to sign the form and send it to Norwegian Swimming Federation by email.


## Prerequisites
- python3

```
pip install -r requirements.txt
```


## Example
```
python transfer-generator.py assets/example.csv
```


## Usage
1. Login into phpmyadmin [https://mysqladmin.it.ntnu.no/](https://mysqladmin.it.ntnu.no/)
2. open members table
3. click on export and use following settings:
```
Format: csv
dump all rows
Columns enclosed with: "
Columns escaped with: "
Put columns names in the first row: true
```

```
python transfer-generator.py member.csv 
```

### Other

[Source Norwegian zip codes](https://www.bring.no/tjenester/adressetjenester/postnummer)

[Source transfer forms](https://svomming.no/forbundet/klubbdrift/organisasjon/overganger/)


### Authors

[Ola Martin Tiseth Støvneng](https://github.com/olamartin)

[Pavel Skipenes](https://github.com/pavelskipenes)
