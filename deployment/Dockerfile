# adapted from the following post
# https://towardsdatascience.com/how-to-do-rapid-prototyping-with-flask-uwsgi-nginx-and-docker-on-openshift-f0ef144033cb


FROM nginx:latest

RUN apt-get update -y && \
    apt-get install -y supervisor uwsgi procps vim python3.5 python3-pip libpcre3 libpcre3-dev&&\
    apt-get install -y poppler-utils tesseract-ocr 

RUN pip3 install uwsgi pipenv

RUN mkdir -p /pdfmagic
COPY ./src pdfmagic/src
WORKDIR /pdfmagic/src

# pipenv install needs these
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# install dependencies
RUN pipenv install --system --deploy --ignore-pipfile

# set up app config
RUN mkdir -p /pdfmagic/uploads /pdfmagic/output
ENV PDFMAGIC_CONFIG /pdfmagic/src/pdfmagic.cfg


# Copy the configuration file from the current directory and paste 
# it inside the container to use it as Nginx's default config.
COPY ./deployment/nginx.conf /etc/nginx/nginx.conf

# setup NGINX config
RUN mkdir -p /spool/nginx /run/pid /var/cache/nginx && \
    chmod -R 777 /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    chgrp -R 0 /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    chmod -R g+rwX /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx
    #rm /etc/nginx/conf.d/default.conf

# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY ./deployment/uwsgi.ini /etc/uwsgi/apps-available/uwsgi.ini
RUN ln -s /etc/uwsgi/apps-available/uwsgi.ini /etc/uwsgi/apps-enabled/uwsgi.ini

COPY ./deployment/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN touch /var/log/supervisor/supervisord.log

EXPOSE 8080:8080

# setup entrypoint
COPY ./deployment/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# https://github.com/moby/moby/issues/31243#issuecomment-406879017
RUN ln -s /usr/local/bin/docker-entrypoint.sh / && \
    chmod 777 /usr/local/bin/docker-entrypoint.sh && \
    chgrp -R 0 /usr/local/bin/docker-entrypoint.sh && \
    chown -R nginx:root /usr/local/bin/docker-entrypoint.sh

# go to link below and search for "Support Arbitrary User IDs"
# https://docs.openshift.com/container-platform/3.3/creating_images/guidelines.html
RUN chgrp -R 0 /var/log /var/cache /run/pid /spool/nginx /var/run /run /tmp /etc/uwsgi /etc/nginx /pdfmagic && \
    chmod -R g+rwX /var/log /var/cache /run/pid /spool/nginx /var/run /run /tmp /etc/uwsgi /etc/nginx /pdfmagic && \
    chown -R nginx:root ${HOME} && \
    chmod -R 777 ${HOME} /etc/passwd


# enter
WORKDIR /pdfmagic
ENTRYPOINT [ "docker-entrypoint.sh" ]
CMD [ "supervisord" ]

