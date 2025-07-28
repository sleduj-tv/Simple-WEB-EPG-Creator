# Simple-WEB-EPG-Creator
Jednoduchý web python skript pre vytvorenie XML-TV EPG.

Simple web python script for creating XML-TV EPG.

Prosty skrypt webowy w języku Python do tworzenia XML-TV EPG.

Potrebuješ EPG pre športové kanály bez neho? Žiadny problém. Vytváraš vlastný TV kanál a chceš jednoducho vytvoriť EPG? Žiadny problém.

Do you need EPG for sports channels that don’t have it? No problem. Are you creating your own TV channel and need an easy way to build an EPG? No problem.

Potrzebujesz EPG dla kanałów sportowych, które go nie mają? Nie ma problemu. Tworzysz własny kanał telewizyjny i potrzebujesz łatwego sposobu na stworzenie EPG? Nie ma problemu.

<img width="1365" height="557" alt="image" src="https://github.com/user-attachments/assets/2a2a27a7-318c-430f-8607-ca98d22a3647" />

## Inštalácia / Installation / Instalacja
```
apt update
apt install python3-tk
pip3 install flask
or
apt install python3-flask
git clone https://github.com/sleduj-tv/Simple-WEB-EPG-Creator
cd Simple-WEB-EPG-Creator
python3 app.py
```

## Použitie / Use / Użycie
```
Select language
Select timezone
Add title of program (e.g. Spongebob Squarepants S07E01)
Add name of TV channel (e.g. Nickelodeon)
Add TVG-ID of TV channel (e.g. 1-nickelodeon)
Add Start time (e.g. 01. 01. 1970 00:00)
Add End time (e.g. 01. 01. 1970 00:00)
Add Description (e.g. Squidward stars in his own TV show; Squidward tries to sabotage SpongeBob's dance audition.)
Add Program
If you need to create next program repeat this procedure.
Export to XMLTV and Download (The file will be saved in your app folder if downloading isn't necessary.)
```
