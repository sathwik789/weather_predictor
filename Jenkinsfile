pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/sathwik789/weather_predictor.git'
        BRANCH = 'main'
        IMAGE_NAME = 'sathwik789/weather_predictor'
        IMAGE_TAG = 'latest'  // You can use "${env.BUILD_NUMBER}" or commit hash for versioning
        DOCKER_CREDS_ID = 'docker-hub-credentials' // Jenkins credentials ID
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo '📦 Checking out source code...'
                git credentialsId: 'github-pat', url: "${REPO_URL}", branch: "${BRANCH}"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🔨 Building updated Docker image...'
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push Updated Image') {
            steps {
                echo '🚀 Pushing updated Docker image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Verify Container (Optional)') {
            steps {
                echo '🧪 Running and testing the updated container...'
                sh '''
                    docker run -d --rm -p 5000:5000 --name test_app ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 5
                    curl -s http://localhost:5000 || echo "App may not be ready yet"
                    docker stop test_app
                '''
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up any leftover containers...'
            sh 'docker rm -f test_app || true'
        }

        success {
            echo '✅ Docker image updated and pushed successfully!'
        }

        failure {
            echo '❌ Pipeline failed during Docker update.'
        }
    }
}
