pipeline {
  agent {
    label 'vagov-general-purpose'
  }

  stages {
    stage('Build') {
      steps {
        script {
          slackSend message: "Scorecard Jenkins build started", color: "good", channel: "scorecard-ci-temp"
          dockerImage = docker.image('jekyll/jekyll:4.0')
          args = "--volume=${pwd()}:/srv/jekyll"

          dockerImage.inside(args) {
              sh 'jekyll build --trace'
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
          slackSend message: "Scorecard Jenkins upload started", color: "good", channel: "scorecard-ci-temp"
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
    success {
      slackSend message: "Scorecard Jenkins build succeeded", color: "good", channel: "scorecard-ci-temp"
    }
    failure {
      slackSend message: "Scorecard Jenkins build *FAILED*!", color: "danger", channel: "scorecard-ci-temp"
      message = sh(returnStdout: true, script: 'wget ${env.BUILD_URL}/consoleText').toString()
      slackSend message: "Logs: ${message}", color: "danger", channel: "scorecard-ci-temp"
    }
  }
}
