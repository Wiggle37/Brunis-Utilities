FROM python:3.9

WORKDIR C:/Users/Miste/Documents/Github/Brunis-Utilites/bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
 
CMD [ "python", "./bot/main.py" ]