pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        REPO_URL = 'https://github.com/sathwik789/weather_predictor.git'
        BRANCH = 'main'
        FLASK_LOG = 'flask.log'
    }

    stages {
        stage('Verify Python 3 Installation') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Clone Repository') {
            steps {
                git credentialsId: 'github-pat', url: "${REPO_URL}", branch: "${BRANCH}"
            }
        }

        stage('Install pip if not present') {
            steps {
                sh '''
                    # Check if pip is installed, if not install it
                    python3 -m ensurepip --upgrade
                    python3 -m pip --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    # Install the dependencies from requirements.txt
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask Application') {
            steps {
                sh '''
                    # Activate virtual environment and run the Flask app
                    python3 app.py
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded!'
        }
        failure {
            echo '❌ Pipeline failed! Check the steps.'
        }
    }
}
