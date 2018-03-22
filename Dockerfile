FROM sd2e/python3:ubuntu17

RUN apt-get update
RUN apt-get install -y libraptor2-dev libjsoncpp1

RUN mkdir -p /opt/scripts

WORKDIR /opt/scripts

ADD . /opt/scripts

RUN pip3 install --upgrade pip

RUN pip3 install /opt/scripts/

# custom wheel for Ubuntu
RUN pip3 install https://github.com/tcmitchell/pySBOL/blob/ubuntu/Ubuntu_16.04_64_3/dist/pySBOL-2.3.0.post11-cp36-none-any.whl?raw=true

CMD python3 -m unittest discover /opt/scripts/tests