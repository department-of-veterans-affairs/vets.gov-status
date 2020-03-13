pipeline {
  agent {
    label 'vetsgov-general-purpose'
  }
  environment {
    // Needed for credstash
    AWS_DEFAULT_REGION = 'us-gov-west-1'
  }
  stages {
    stage('Unit tests') {
      steps {
        script {
          sh './run-ci-tests.sh'  // this copies results into ./results directory
        }
      }
      post {
        always {
          junit testResults: 'results/unit/pytest-unit.xml'
        }
        success {
          archiveArtifacts artifacts: "results/coverage/**"
          publishHTML(target: [reportDir: 'results/coverage', reportFiles: 'index.html', reportName: 'Coverage', keepAll: true])
        }
      }
    }

    // Temporary - this stage should be removed and only run in Jenkinsfile.update
    stage('Update Data') {
      steps{
        script {
          dir('scripts') {
            sh './run-ci-fetch-data.sh'
          }
        }
      }
    }

    stage('Build website') {
      steps {
        script {
          // slackSend message: "Scorecard Jenkins build started", color: "good", channel: "scorecard-ci-temp"
          nodeImg = docker.image('node:12.16.1')
          nodeImg.inside() {
            sh 'yarn install --frozen-lockfile --production=true'
          }

          jekyllImg = docker.image('jekyll/jekyll:4.0')
          args = "--volume=${pwd()}:/srv/jekyll"
          jekyllImg.inside(args) {
            sh '/usr/gem/bin/jekyll build --trace'
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
          // slackSend message: "Scorecard Jenkins upload started", color: "good", channel: "scorecard-ci-temp"
          def envs = [
            'demo': ['dev'],
            'master': ['staging'],
            'production': ['staging'],  // todo: point this back to production once we are ready to golive
          ]

          for (e in envs.get(env.BRANCH_NAME, [])) {
            sh "bash --login -c 'aws s3 sync --acl public-read --delete --region us-gov-west-1 _site s3://dsva-vetsgov-scorecard-${e}/'"
            slackSend message: "Dashboard deployed to ${e} environment", color: "good", channel: "scorecard-ci-temp"
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
      echo "Build success"
      // slackSend message: "Scorecard Jenkins build succeeded", color: "good", channel: "scorecard-ci-temp"
    }
    failure {
      echo "Build failure"
      // slackSend message: "Scorecard Jenkins build *FAILED*!", color: "danger", channel: "scorecard-ci-temp"
    }
  }
}
