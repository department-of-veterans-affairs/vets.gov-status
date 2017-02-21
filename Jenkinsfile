pipeline {
  agent {
    label 'rails-testing'
  }

  stages {
    stage('Checkout Code') {
      steps {
        checkout scm
      }
    }

    stage('Build') {
      steps {
        sh 'bash --login -c "bundle"'
        sh 'bash --login -c "bundle exec jekyll build"'
      }
    }

    stage('Upload') {
      when {
        expression {
          (env.BRANCH_NAME == 'master' ||
          env.BRANCH_NAME == 'production') &&
          !env.CHANGE_TARGET
        }
      }
      steps {
        script {
          def envs = [
            'master': ['dev', 'staging'],
            'production': ['prod'],
          ]

          for (e in envs.get(env.BRANCH_NAME, [])) {
            sh "bash --login -c 'aws s3 sync --acl public-read --delete --region us-gov-west-1 _site s3://dsva-vetsgov-scorecard-${e}/'"
          }
        }
      }
    }
  }
}
