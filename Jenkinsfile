#!/usr/bin/env groovy
node {
  def environment = null
  stage('Configure tailor-distro') {
    checkout scm
    environment = docker.build("environment", "environment")
  }
  stage('Pull source') {
    milestone(1)
    node {
      environment.inside {
        sh 'pip3 install .'
        sh 'pull_distro'
      }
    }
    cleanWs()
  }



}
