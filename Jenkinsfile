pipeline {
    // Run every stage inside your own image, built from the Dockerfile.
    // Requires the Docker Pipeline plugin and Docker available on the agent.
    agent {
        dockerfile {
            filename 'Dockerfile'
            // --ipc=host avoids Chromium crashing on small /dev/shm in CI.
            args '--ipc=host'
        }
    }

    options {
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {
        stage('Test') {
            // Credentials pulled from the Jenkins Credentials store and exposed
            // as env vars for the duration of this stage. Create these as
            // "Secret text" credentials with matching IDs.
            environment {
                API_USER_EMAIL    = credentials('api-user-email')
                API_USER_PASSWORD = credentials('api-user-password')
                UI_USER_EMAIL     = credentials('ui-user-email')
                UI_USER_PASSWORD  = credentials('ui-user-password')
            }
            steps {
                // Image already has deps + browsers; just run the suite.
                sh '''pytest playwright_course \
                        --junitxml=results.xml \
                        --html=report.html --self-contained-html \
                        -v'''
            }
        }
    }

    post {
        always {
            // Surface pass/fail per test in the Jenkins UI.
            junit 'results.xml'
            // Keep the HTML report as a downloadable build artifact.
            // (For an inline view, install the HTML Publisher plugin and use
            // publishHTML instead.)
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
        }
    }
}