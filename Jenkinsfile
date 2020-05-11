pipeline {
  agent { label 'master' }
  options {
    timeout(time: 60, unit: 'MINUTES')
  }

  stages {
    stage ('Checkout') {
      steps {
        checkoutSubmodule()
      }
    }

    stage ('Pre-commit Checks') {
      steps {
        script {
          REPO_NAME = env.JOB_NAME.split('/')[1]
          PKG_NAME  = REPO_NAME.substring(0, REPO_NAME.length() - 4)
          dir(PKG_NAME) {
            preCommit()
          }
        }
      }
    }

    stage ('Build') {
      steps {
        withCredentials([string(credentialsId: 'further-link-key', variable: 'key')]) {
          sh 'python3 -c "import codecs; print(codecs.getencoder(\'rot-13\')(\'$key\')[0])" > pt-further-link/data'
        }
        buildDebPkg()
      }
    }

    stage ('Test') {
      steps {
        checkSymLinks()
        // shellcheck()

        sh """
        cd pt-further-link
        pipenv sync --dev
        FURTHER_LINK_WORK_DIR=\$(pwd) pipenv run pytest test.py
        """

        script {
          try {
            lintian()
          } catch (e) {
            currentBuild.result = 'UNSTABLE'
          }
        }
      }
    }

    stage ('Publish') {
      steps {
        publishSirius()
      }
    }
  }
}
