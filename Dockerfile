FROM python:3.9

WORKDIR /Users/Miste/Documents/Github/Brunis-Utilites/bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
 
CMD [ "python3", "main.py" ]