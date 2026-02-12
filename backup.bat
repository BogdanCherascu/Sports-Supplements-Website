@echo off

IF EXIST backup.sql DEL backup.sql

SET PGPASSWORD=bogdan

ECHO Pornire backup...

FOR %%t IN (
    "magazin_categorie"
    "magazin_produs"
    "magazin_producator"
    "magazin_ingredient"
    "magazin_oferta"
) DO (
    ECHO Backup pentru tabelul %%t
    pg_dump --column-inserts --data-only --inserts ^
    -h localhost ^
    -U bogdan ^
    -p 5432 ^
    -d projectsuplimente ^
    -t %%t >> backup.sql
)

SET PGPASSWORD=

ECHO Backup finalizat!
PAUSE
