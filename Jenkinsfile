pipeline {
    agent any

    environment {
        VENV_PATH = 'venv'
        FLASK_APP_PATH = 'workspace/webapp/app.py'
        PATH = "$VENV_PATH/bin:$PATH"
    }
    
    stages {
        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }
        
        stage('Clone Repository') {
            steps {
                dir('workspace') {
                    git branch: 'main', url: 'https://github.com/SelenaxPS/ICT2216_Practical'
                }
            }
        }
        
        stage('Setup Virtual Environment') {
            steps {
                dir('workspace/webapp') {
                    sh 'python3 -m venv $VENV_PATH'
                }
            }
        }
        
        stage('Activate Virtual Environment and Install Dependencies') {
            steps {
                dir('workspace/webapp') {
                    sh '''
                        set +e
                        source $VENV_PATH/bin/activate
                        pip install -r requirements.txt
                        set -e
                    '''
                }
            }
        }
        
		stage('Integration Testing') {
            steps {
                dir('workspace/webapp') {
                    sh '''
                        set +e
                        source $VENV_PATH/bin/activate
                        pytest --junitxml=integration-test-results.xml
                        set -e
                    '''
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                dir('workspace/webapp') {
                    sh 'docker build -t flask-app .'
                }
            }
        }
        
        stage('Deploy Flask App') {
            steps {
                script {
                    echo 'Deploying Flask App...'
                    sh 'docker ps --filter publish=5000 --format "{{.ID}}" | xargs -r docker stop'
                    sh 'docker ps -a --filter status=exited --filter publish=5000 --format "{{.ID}}" | xargs -r docker rm'
                    sh 'docker run -d -p 5000:5000 flask-app'
                    sh 'sleep 10'
                }
            }
        }
    }
    
    post {
        failure {
            script {
                echo 'Build failed, not deploying Flask app.'
            }
        }
        always {
            archiveArtifacts artifacts: 'workspace/webapp/integration-test-results.xml', allowEmptyArchive: true
        }
    }
}
