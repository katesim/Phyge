FROM python:3.6

COPY app/requirements.txt /usr/tmp/
RUN pip install --upgrade pip
RUN cat /usr/tmp/requirements.txt
RUN pip install -r /usr/tmp/requirements.txt

RUN cd /tmp && \
		git clone https://github.com/buriy/python-readability && \
		cd python-readability && \
		python setup.py install

# Make project dir
RUN mkdir /apps

CMD ["/bin/bash"]

EXPOSE 5050
