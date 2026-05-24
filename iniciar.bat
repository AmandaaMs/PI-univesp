@echo off
echo Iniciando MDS...

REM instala dependencias
python -m pip install -r requirements.txt

REM inicia o servidor em segundo plano
start cmd /k python run.py

REM espera 5 segundos
timeout /t 5 > nul

REM abre o navegador
start http://127.0.0.1:5000

echo Sistema iniciado com sucesso!
pause