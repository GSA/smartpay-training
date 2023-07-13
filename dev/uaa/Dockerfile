FROM eclipse-temurin:11-jdk

ENV UAA_VERSION=76.14.0

WORKDIR /tmp

RUN wget -q https://github.com/cloudfoundry/uaa/archive/refs/tags/v${UAA_VERSION}.tar.gz -O /tmp/uaa.tar.gz
RUN mkdir -p /tmp/uaa && tar xf uaa.tar.gz -C /tmp/uaa --strip-components=1

WORKDIR /tmp/uaa

EXPOSE 8080

CMD ["sh", "-c", "/tmp/uaa/gradlew run"]
