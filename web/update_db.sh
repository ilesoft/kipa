#!/bin/bash

rm -r fixtures/old.xml
echo Luodaan legacy datamalli legacy/models.py
python manage.py inspectlegacy
echo Kopioidaan vanha data tiedostoon fixtures/old.xml
python manage.py dumpdata legacy --format=xml --indent=4 > fixtures/old.xml
python legacy/RenameFixture.py 
echo Luodaan uuden tietokannan malli tupa/tietokata.dia tiedostosta models.py tiedostoon.
python tupa/dia2django.py tupa/tietokanta.dia tupa/models.py
echo Nollataan ja päivitetään tietokantataulut.
python manage.py reset --noinput tupa
echo Ladataan fixturen data uuteen tietokantaan.
python manage.py loaddata fixture fixtures/old.xml
echo old.xml
python manage.py loaddata fixture fixtures/old.xml


