pipeline {
    agent any

    environment {
        VENV_PATH = "${WORKSPACE}/venv"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/ragulmuthu03/VAPT-Project-Phase-2.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install --no-cache-dir -r requirements.txt
                pip install pylint
                '''
            }
        }

        stage('Run Code Linting') {
            steps {
                sh '''
                . venv/bin/activate
                export PATH=$WORKSPACE/venv/bin:$PATH
                which pylint  # Debugging step
                pylint --fail-under=6.0 tidconsole.py || true
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                . venv/bin/activate
                export PATH=$WORKSPACE/venv/bin:$PATH
                python -m unittest discover -s tests
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                chmod +x docker  # Ensure Docker has execute permissions
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

