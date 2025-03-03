pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/ragulmuthu03/VAPT-Project-Phase-2.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install --no-cache-dir -r requirements.txt
                '''
            }
        }

        stage('Run Code Linting') {
            steps {
                sh '''
                source venv/bin/activate
                venv/bin/pylint tidconsole.py
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                source venv/bin/activate
                python -m unittest discover -s tests
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t vapt-cli .
                '''
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh '''
                docker run -p 5001:5000 -dit --name vapt-container vapt-cli
                '''
            }
        }

        stage('Approval for Production') {
            steps {
                input message: "Deploy to Production?", ok: "Deploy"
            }
        }

        stage('Deploy to Production') {
            steps {
                sh '''
                docker tag vapt-cli myrepo/vapt-cli:latest
                docker push myrepo/vapt-cli:latest
                '''
            }
        }
    }
}

