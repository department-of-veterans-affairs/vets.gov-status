FROM jekyll/jekyll

# Match the jenkins uid/gid on the host (504)
RUN addgroup -g 504 jenkins \
  && adduser -D -u 504 -G jenkins jenkins

RUN chown jenkins:jenkins /srv/jekyll
RUN chown jenkins:jenkins /home/jenkins
USER jenkins
