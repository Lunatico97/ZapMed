FROM python:3.11

label maintainer = "adiwas47@gmail.com"

RUN apt-get update

RUN pip3 install --upgrade pip

WORKDIR /

COPY requirements.txt /

RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY src /

ENTRYPOINT ["streamlit", "run"]

CMD ["src/app.py"]
