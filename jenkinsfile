pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Setup') {
      steps { sh 'python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements-dev.txt' }
    }
    stage('Test')  { steps { sh '. .venv/bin/activate && pytest -q' } }
    stage('Lint')  { steps { sh '. .venv/bin/activate && ruff check .' } }
    stage('SAST - Bandit')  { steps { sh '. .venv/bin/activate && bandit -r app/ -f txt' } }
    stage('SAST - Semgrep') { steps { sh '. .venv/bin/activate && semgrep --config auto app/' } }
    stage('SCA - pip-audit') { steps { sh '. .venv/bin/activate && pip-audit -r requirements.txt' } }
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
