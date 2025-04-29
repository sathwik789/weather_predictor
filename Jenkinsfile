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

        stage('Create Virtual Environment') {
            steps {
                sh '''
                    # Create a virtual environment if it doesn't already exist
                    python3 -m venv ${VENV_DIR}
                    # Activate the virtual environment
                    source ${VENV_DIR}/bin/activate
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    # Activate the virtual environment and install dependencies
                    source ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask Application') {
            steps {
                sh '''
                    # Activate the virtual environment and run the Flask app
                    source ${VENV_DIR}/bin/activate
                    python app.py
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
