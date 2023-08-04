# For best results, match version in use by cloud.gov RDS
FROM postgres:12

ADD generate-cert.sh /tmp/generate-cert.sh

RUN /tmp/generate-cert.sh
