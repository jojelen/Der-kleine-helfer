# Der kleine Helfer

Retrieves a number of food recipes from data dir, combines a grocery list and
sends out an email with list, instructions and possibly pdfs.

# Requirements

## Data

The script parses all json files in datadir. The json file should contain
elements like

```
{"recept": "Cooked potato",  "url": "https://www.potato.se/", "ingredients":
[{"name": "Potato", "quantity": "500", "unit": "g"}, {"name": "Water",
"quantity": "2", "unit": "l"}], "instructions": ["Cook potato", "Serve"]}
```

## Config

Create a 'config.ini' file with the following information:

```
[run]
tmpdir = /tmp/der-kleine-helfer
datadir = /data-dir-containing-json

[mail]
tls = true
smtp = smtp.office365.com
port = 587
sender = your_email@hotmail.com
password = pass
reciever = Joe <joe@hotmail.com>:Philly <philly@web.de>
```
