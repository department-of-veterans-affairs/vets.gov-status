pipeline {
  agent {
    label 'vagov-general-purpose'
  }

  stages {
    stage('Build') {
      steps {
        script {
          dockerImage = docker.image('jekyll/jekyll')
          args = "-v ${pwd()}:/srv/jekyll"
          dockerImage.inside(args) {
            sh '/usr/gem/bin/jekyll build'
          }
        }
      }
    }

    stage('Upload') {
      when {
        expression {
          (env.BRANCH_NAME == 'demo' ||
          env.BRANCH_NAME == 'master' ||
          env.BRANCH_NAME == 'production') &&
          !env.CHANGE_TARGET
        }
      }
      steps {
        script {
          def envs = [
            'demo': ['dev'],
            'master': ['staging'],
            'production': ['prod'],
          ]

          for (e in envs.get(env.BRANCH_NAME, [])) {
            sh "bash --login -c 'aws s3 sync --acl public-read --delete --region us-gov-west-1 _site s3://dsva-vetsgov-scorecard-${e}/'"
          }
        }
      }
    }
  }
  post {
    always {
      deleteDir() /* clean up our workspace */
    }
  }
}
