pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        REPO_URL = 'https://github.com/sathwik789/weather_predictor.git'
        BRANCH = 'main'
        FLASK_LOG = 'flask.log'
        IMAGE_NAME = 'sathwik789/weather_predictor'
        IMAGE_TAG = 'latest'
        DOCKER_CREDS_ID = 'docker-hub-credentials' // replace with your Jenkins credentials ID for Docker Hub
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

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }

        // Optional: run the container to test
        stage('Test Container') {
            steps {
                sh '''
                    docker run -d --rm -p 5000:5000 --name test_weather_app ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 5
                    curl -s http://localhost:5000 || echo "App might still be starting"
                    docker stop test_weather_app
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline with Docker succeeded!'
        }
        failure {
            echo '❌ Pipeline failed! Check Docker build/push steps.'
        }
    }
}
