pipeline {
    agent any

    environment {
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

        stage('Install Dependencies') {
            steps {
                sh '''
                    # Install dependencies globally
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask Application') {
            steps {
                sh '''
                    # Run your Flask application
                    export FLASK_APP=app.py
                    export FLASK_ENV=development
                    flask run --host=0.0.0.0 --port=5000
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded! Flask app is running.'
        }
        failure {
            echo '❌ Pipeline failed! Check the steps.'
        }
    }
}
