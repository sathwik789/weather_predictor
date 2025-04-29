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

        // Optional: run the app (if you want to test without Docker)
        stage('Run Application') {
            steps {
                sh '''
                    # Create and activate virtual environment
                    python3 -m venv ${VENV_DIR}
                    source ${VENV_DIR}/bin/activate
                    
                    # Install dependencies
                    pip install -r requirements.txt

                    # Run the Flask app (replace with your actual command)
                    nohup flask run --host=0.0.0.0 --port=5000 > ${FLASK_LOG} 2>&1 &
                    sleep 5
                    curl -s http://localhost:5000 || echo "App might still be starting"
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
