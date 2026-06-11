pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Setup') {
      steps { sh 'pip install -r requirements-dev.txt --break-system-packages' }
    }
    stage('Test')  { steps { sh 'pytest -q' } }
    stage('Lint')  { steps { sh 'ruff check .' } }
    stage('SAST - Bandit')  { steps { sh 'bandit -r app/ -f txt' } }
    stage('SAST - Semgrep') { steps { sh 'semgrep --config auto app/' } }
    stage('SCA - pip-audit') { steps { sh 'pip-audit -r requirements.txt' } }
    stage('Secrets - Gitleaks') {
      steps { sh 'docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:latest detect --source=/repo -v' }
    }
    stage('FS Scan - Trivy') {
      steps { sh 'docker run --rm -v "$PWD:/repo" aquasec/trivy:latest fs /repo' }
    }
    stage('Build Image') { steps { sh 'docker build -t flask-api:${BUILD_NUMBER} .' } }
  }
  post {
    always { archiveArtifacts artifacts: 'bandit.txt', allowEmptyArchive: true }
  }
}
