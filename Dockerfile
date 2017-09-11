FROM jekyll/jekyll

# Match the jenkins uid/gid on the host (504)
RUN addgroup -Sg 504 jenkins \
  && adduser -S -u 504 -G jenkins -h /home/jenkins jenkins

RUN chown -R jenkins:jenkins /srv/jekyll
RUN chown -R jenkins:jenkins /home/jenkins
USER jenkins
