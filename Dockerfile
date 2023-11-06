FROM python:3
COPY . . 
RUN python3 -m pip install -r requirements.txt
EXPOSE 8000
CMD [ "python3", 'main,py']