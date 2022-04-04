# Swimming transfer form generator

auto generate transfer forms ("overgangsskjema") for new members

# Prerequisites
TODO: add required packages

# Usage
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

# Download updated zip codes
[https://www.bring.no/tjenester/adressetjenester/postnummer](https://www.bring.no/tjenester/adressetjenester/postnummer)


# Download new transfer forms
[https://svomming.no/forbundet/klubbdrift/organisasjon/overganger/](https://svomming.no/forbundet/klubbdrift/organisasjon/overganger/)