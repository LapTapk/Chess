cd %~d0
if exist .venv\Scripts\activate.bat (
    echo
) else (
 python -m virtualenv .venv
 CALL .venv\Scripts\activate.bat
 pip install pygame
 pip install setuptools
 python setup.py install
)
 python src/main.py