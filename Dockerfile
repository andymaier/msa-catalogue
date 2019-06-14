FROM openjdk
ENV host=172.17.0.2
COPY target/*.jar .

CMD ["java","-jar","catalogue-1.0.0.jar","--spring.cloud.consul.host=consul"]
