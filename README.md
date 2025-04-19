How to execute the code?
1. cd StockTracker
2. source venv1/bin/activate
3. python manage.py runserver 0.0.0.0:8000

Run in the background, you can close the power shell
nohup python manage.py runserver 0.0.0.0:8000 &

Stop running the server
pkill -f manage.py

How to end the server?
Ctrl+C

How to exit the virtual environment?
deactivate
