pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/ragulmuthu03/VAPT-Project-Phase-2.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh 'python3 -m venv $VENV_DIR'
                sh '. venv/bin/activate && pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Run Code Linting') {
            steps {
                sh 'pylint tidconsole.py'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh 'pytest tests/'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t vapt-cli .'
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh 'docker run -p 5001:5000 -dit --name vapt-container vapt-cli'
            }
        }

        stage('Approval for Production') {
            steps {
                input message: 'Deploy to Production?', ok: 'Yes, Deploy'
            }
        }

        stage('Deploy to Production') {
            steps {
                sh 'docker stop vapt-container || true'
                sh 'docker rm vapt-container || true'
                sh 'docker run -p 5001:5000 -dit --name vapt-container vapt-cli'
            }
        }
    }
}
