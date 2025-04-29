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

        stage('Set Up Virtual Environment and Install Dependencies') {
            steps {
                sh '''
                    # Create and activate virtual environment
                    python3 -m venv ${VENV_DIR}
                    source ${VENV_DIR}/bin/activate
                    
                    # Install dependencies from requirements.txt
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask Application') {
            steps {
                sh '''
                    # Run the Flask app in the background
                    nohup flask run --host=0.0.0.0 --port=5000 > ${FLASK_LOG} 2>&1 &
                    sleep 5
                    
                    # Test if the app is running
                    curl -s http://localhost:5000 || echo "App might still be starting"
                    
                    # Stop the Flask app
                    pkill -f flask
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
