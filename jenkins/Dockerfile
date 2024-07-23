FROM jenkins/jenkins:lts
USER root

ENV JENKINS_USER admin
ENV JENKINS_PASS Raymond


#id_rsa.pub file will be saved at /root/.ssh/
RUN ssh-keygen -f /root/.ssh/id_rsa -t rsa -N ''  


# allows to skip Jenkins setup wizard
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false

# Jenkins runs all grovy files from init.groovy.d dir
# use this for creating default admin user
COPY default-user.groovy /usr/share/jenkins/ref/init.groovy.d/

VOLUME /var/jenkins_home 

# Install Python and Docker CLI
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv docker.io && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# Install docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/2.29.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose
	
# Add Jenkins user to Docker group
RUN usermod -aG docker jenkins

USER jenkins
