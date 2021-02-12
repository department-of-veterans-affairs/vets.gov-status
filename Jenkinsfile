pipeline {
  agent {
    label 'vetsgov-general-purpose'
  }
  environment {
    // Needed for credstash
    AWS_DEFAULT_REGION = 'us-gov-west-1'
    // Variable used in makefile to determine behavior of some scripts
    CI = "true"
  }
  options {
    ansiColor('xterm')
  }
  stages {
    stage('Unit tests') {
      steps {
        script {
          sh 'make ci-unit-test'  // this copies results into ./results directory
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

    stage('Data fetch integration test') {
      steps{
        script {
          sh 'make integration-test'
        }
      }
    }

    stage('Build website') {
      steps {
        script {
          nodeImg = docker.image('node:12.20.1')
          nodeImg.inside() {
            sh 'make yarn-install'
          }

          jekyllImg = docker.image('jekyll/jekyll:4.0')
          args = "--volume=${pwd()}:/srv/jekyll"
          jekyllImg.inside(args) {
            sh '/usr/gem/bin/jekyll build --trace'
          }
        }
      }
    }

    stage('UI tests') {
      steps {
        script {
          docker.image('circleci/node:12.20.1-buster-browsers').inside() {
            sh 'make ci-ui-test'
          }
        }
      }
    }

    stage('Upload') {
      when {
        expression {
          (env.BRANCH_NAME == 'development' ||
          env.BRANCH_NAME == 'master' ||
          env.BRANCH_NAME == 'production') &&
          !env.CHANGE_TARGET
        }
      }
      steps {
        script {
          def envs = [
            'development': ['dev'],
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
      echo "Build success"
    }
    failure {
      echo "Build failure"
    }
  }
}
