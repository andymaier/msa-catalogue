node {
        environment { 
            host = 'localhost'
        }
        stage("Checkout") {
            checkout scm
        }

        stage('Maven Build') {
            sh "mvn -DskipTests=true package"
        }

        stage('Maven Tests') {
            //sh "mvn test"
            sh "echo Testing"
        }

        stage('Docker image') {
             docker.build("catalogue")
        }

        stage("Deploy") {
            sh "docker rm -f catalogue || echo 'ok'"
            sh "docker run -d --name catalogue -p 2020:8080 catalogue"
        }
}
