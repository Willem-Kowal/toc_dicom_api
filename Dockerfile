FROM python:3.8-slim-buster

WORKDIR /src

RUN pip install flask
RUN pip install numpy
RUN pip install pytest
RUN pip install pydicom
RUN pip install pypng
RUN pip install "connexion[flask,uvicorn,swagger-ui]"

copy . .

CMD [ "python", "-m", "toy_dicom_api.__init__"]
