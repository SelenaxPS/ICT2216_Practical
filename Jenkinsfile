pipeline {
    agent any

    environment {
        VENV_PATH = 'venv'
        FLASK_APP_PATH = 'workspace/webapp/app.py'
        PATH = "$VENV_PATH/bin:$PATH"
        SONARQUBE_SCANNER_HOME = tool name: 'SonarQube Scanner'
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
                        #!/bin/bash
                        set +e
                        source $VENV_PATH/bin/activate
                        pip install -r requirements.txt
                        pip install webdriver-manager
                        set -e
                    '''
                }
            }
        }

        stage('Install Chrome and ChromeDriver') {
            steps {
                sh '''
                    #!/bin/bash
                    set +e
                    if ! command -v google-chrome &> /dev/null
                    then
                        echo "Installing Google Chrome..."
                        wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
                        sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
                        sudo apt-get update
                        sudo apt-get install -y google-chrome-stable
                    fi
                    set -e
                '''
            }
        }

        stage('Integration Testing') {
            steps {
                dir('workspace/webapp') {
                    sh '''
                        #!/bin/bash
                        set +e
                        source $VENV_PATH/bin/activate
                        pytest --junitxml=integration-test-results.xml
                        set -e
                    '''
                }
            }
        }

        stage('OWASP DependencyCheck') {
            steps {
                withCredentials([string(credentialsId: 'NVD_API_KEY', variable: 'NVD_API_KEY')]) {
                    dependencyCheck additionalArguments: "-o './' -s './' -f 'ALL' --prettyPrint --nvdApiKey ${env.NVD_API_KEY}", odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
                    dependencyCheckPublisher pattern: 'dependency-check-report.xml'
                }
            }
        }
		
        stage('UI Testing') {
            steps {
                dir('workspace/webapp') {
                    sh '''
                        #!/bin/bash
                        set +e
                        source $VENV_PATH/bin/activate
                        pytest tests/ui --junitxml=ui-test-results.xml
                        set -e
                    '''
                }
            }
        }
 
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    withCredentials([string(credentialsId: 'SONARQUBE_KEY', variable: 'SONARQUBE_TOKEN')]) {
                        dir('workspace/flask') {
                            sh '''
                            #!/bin/bash
                            ${SONARQUBE_SCANNER_HOME}/bin/sonar-scanner \
                            -Dsonar.projectKey=flask-app \
                            -Dsonar.sources=. \
                            -Dsonar.inclusions=app.py \
                            -Dsonar.host.url=http://sonarqube:9000 \
                            -Dsonar.login=${SONARQUBE_TOKEN}
                            '''
                        }
                    }
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
            archiveArtifacts artifacts: 'workspace/webapp/ui-test-results.xml', allowEmptyArchive: true
        }
    }
}
