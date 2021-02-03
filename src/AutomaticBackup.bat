@ECHO OFF
set postgresAddress="D:\Program Files\PostgreSQL\12\bin"
set PGPASSWORD=mypassword
set MYDBNAME=postgres
set MYDBUSER=postgres


set var=%cd%
mkdir backups


:loop
    set _my_datetime=%date%_%time%
    set _my_datetime=%_my_datetime: =_%
    set _my_datetime=%_my_datetime::=%
    set _my_datetime=%_my_datetime:/=_%
    set _my_datetime=%_my_datetime:.=_%

    cd %postgresAddress%
    .\pg_dump.exe -U %MYDBUSER% %MYDBNAME% > %var%\backups\backup_%_my_datetime%.bac
    cd %var%
    echo Last backup in %date% %time%!
    ping 192.0.2.2 -n 1 -w 5000 > nul
goto loop

cd %var%