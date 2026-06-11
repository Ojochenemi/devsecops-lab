pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Setup') {
      steps { sh 'pip install -r requirements.txt -r requirements-dev.txt --break-system-packages' }
    }
    stage('Test')  { steps { sh 'python3.13 -m pytest tests/ -q' } }
    stage('Lint')  { steps { sh 'python3.13 -m ruff check .' } }
    stage('SAST - Bandit')  { steps { sh 'python3.13 -m bandit -r app/ -f txt' } }
    stage('SAST - Semgrep') { steps { sh 'python3.13 -m semgrep --config auto app/' } }
    stage('SCA - pip-audit') { steps { sh 'python3.13 -m pip_audit -r requirements.txt' } }
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
