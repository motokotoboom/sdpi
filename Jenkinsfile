pipeline{
    agent any

    stages {
        stage('Get source') {
            steps {
                echo 'getting source'
                checkout scm
            }
        }
        stage('running php-apache'){
            steps{
                echo 'run flask app'           
                sh '''
                    ls -l /var/www/
                    echo $JOB_NAME
                    echo $WORKSPACE
                    echo $JENKINS_HOME
                '''
            }
        }

    }
}
