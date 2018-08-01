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
                    if [ -d /var/www/$JOB_NAME ]; then 
                        echo  \"already exists\"
                    else
                         mkdir /var/www/$JOB_NAME
                    fi
                    
    
                    cp -rf $WORKSPACE/* /var/www/$JOB_NAME
                    echo $JOB_NAME
                    echo $WORKSPACE
                    echo $JENKINS_HOME
                '''
                sh '''
                if [ \"`docker service ls --filter=\"name=sdpi\" | wc -l`\" != \"2\" ]; then
                docker run -d --name=sdpi -p 5000:5000  --mount type=volume,volume-driver=local,dst=/var/www,volume-opt=type=nfs,volume-opt=device=:/var/www/,volume-opt=o=addr=$(cat /tmp/host),volume-nocopy=true -v /var/run/docker.sock:/var/run/docker.sock motokotoboom/sdpi:latest
                fi
                '''
            }
        }
    }
}
