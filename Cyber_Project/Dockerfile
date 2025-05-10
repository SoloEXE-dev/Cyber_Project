
FROM ubuntu

RUN apt-get clean
RUN apt-get update
RUN apt-get install -y openssh-server
RUN apt-get install -y openssh-client
RUN apt-get install -y rsync
RUN apt-get install -y cron
RUN apt-get install -y nano
RUN apt-get install -y vim
RUN apt-get install -y python3-dev --fix-missing
RUN apt-get install -y pip
RUN pip install cryptography.fernet --break-system-packages
RUN pip install paramiko --break-system-packages
RUN mkdir /var/run/sshd
RUN mkdir /main
RUN mkdir /backup
RUN mkdir /programs
RUN echo "root:password" | chpasswd
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
RUN (crontab -l ; echo "#* * * * * echo "Hello world" >> /var/log/cron.log") | crontab
RUN (crontab -l ; echo "#00 15 * * * /bin/sh /program/cloudup.sh") | crontab
RUN (crontab -l ; echo "#* * * * * /usr/bin/python3 /program/reader.py") | crontab
ADD removedata.sh cloudup.sh reback.sh reader.py jumpjump.py /programs/
COPY ./dummy/ /main/dummy/
CMD service cron start && /usr/sbin/sshd -D