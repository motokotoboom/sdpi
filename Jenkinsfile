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
                    ip address show eth0 | sed -nr 's/.*inet ([^\\/]+).*/\\1/p' > /tmp/host
                    mkdir /var/www/$JOB_NAME
    
                    cp -rf $WORKSPACE /var/www/$JOB_NAME
                    sudo export 
                    echo $JOB_NAME
                    echo $WORKSPACE
                    echo $JENKINS_HOME
                '''
                sh '''
                if [ \"`docker service ls --filter=\"name=sdpi\" | wc -l`\" != \"2\" ]; then
                docker run --name=sdpi -p 5000:5000  --mount type=volume,volume-driver=local,dst=/var/www,volume-opt=type=nfs,volume-opt=device=:/var/www/,volume-opt=o=addr=$(cat /tmp/host),volume-nocopy=true -v /var/run/docker.socket:/var/run/socket motokotoboom/sdpi:latest
                fi
                '''
            }
        }
    }
}
