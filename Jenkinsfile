import org.kohsuke.github.GitHub

def PR = 0

def create_pr = {
  def github = GitHub.connect()

  def now = new Date().format('yyyy-MM-dd')
  def update_branch = "refs/heads/update-${now}"
  def target_branch = 'refs/heads/master'

  def pr_title = "Automatic Data Update on ${now}"
  def pr_body = 'Automatic Data Update run from Jenkins'

  def repo = github.getRepository('department-of-veterans-affairs/vets.gov-status')

  def pr = repo.createPullRequest(pr_title, update_branch, target_branch, pr_body)

  PR = pr.getNumber()
}

def merge_pr = {
  def github = GitHub.connect()
  def repo = github.getRepository('department-of-veterans-affairs/vets.gov-status')
  def pr = repo.getPullRequest(PR)

  def is_mergeable = true

  // Do basic checks of mergeability
  if (!pr.getMergeable() || pr.getMergeableState() != 'clean') {
    is_mergeable = false
  }

  if (is_mergeable) {
    pr.merge('Merged automatically by Jenkins.')

    //Delete extraneous branch
    def now = new Date().format('yyyy-MM-dd')
    def update_branch = "heads/update-${now}"
    def ref = repo.getRef(update_branch)
    ref.delete()
  } else {
    pr.comment('Skipping merge!')
  }
}

pipeline {
  agent {
    label 'vetsgov-general-purpose'
  }
  environment {
    // Needed for credstash
    AWS_DEFAULT_REGION = 'us-gov-west-1'

    GH = credentials('va-bot')
  }

  stages {

    stage('Setup Update Branch') {
      steps {
        sh 'git config user.name "va-bot"'
        sh 'git config user.email "james.kassemi+vabot@adhocteam.us"'
        sh 'git checkout -b update-$(date -I)'
      }
    }

    stage('Update Data') {
      steps{
        script {
          dir('scripts') {
            sh './run-ci-fetch-data.sh'
          }
        }
      }
    }

    stage('Push Update Branch to Github') {
      steps {
        sh 'git add .'
        sh "git commit -m 'Updated Data'"
        sh 'git push https://${GH_USR}:${GH_PSW}@github.com/department-of-veterans-affairs/vets.gov-status.git HEAD'
      }
    }

    stage('Create PR'){
      steps {
        script { create_pr() }
      }
    }

    stage ('Wait for PR Status to Update') {
      steps {
        timeout(time: 1, unit: 'HOURS') {
          waitUntil {
            sleep time: 1, unit: 'MINUTES'
            script {
              def github = GitHub.connect()
              def repo = github.getRepository('department-of-veterans-affairs/vets.gov-status')
              def pr = repo.getPullRequest(PR)
              return (pr.getMergeable() != null)
            }
          }
        }
      }
    }

    stage('Merge PR and Delete Branch') {
      steps {
        script { merge_pr() }
      }
    }
  }

  post {
    always {
      deleteDir()
    }
    success {
      slackSend message: "Performance dashboard data update succeeded", color: "good", channel: "scorecard-ci-temp"
    }
    failure {
      slackSend message: "<!here> Performance dashboard data update *FAILED*!", color: "danger", channel: "scorecard-ci-temp"
    }
  }
}
