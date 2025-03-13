# Gitlab CI/CD

GitLab CI/CD automates software development by continuously building, testing,
deploying, and monitoring code changes, ensuring stable and high-quality releases.
It helps catch bugs early and enforces coding standards.

This guide is based on the [official documentation](https://docs.gitlab.com/ci/)

## Steps to Get Started

### Create a ```.gitlab-ci.yml file```

- Defines stages, jobs, and scripts for the CI/CD pipeline.
- Uses YAML syntax to specify variables, dependencies, and execution conditions.

### Find or Create Runners

- Runners execute jobs, either on physical machines or virtual instances.
- GitLab.com provides built-in runners for Linux, Windows, and macOS.
- Self-managed users must register their own runners.

### Define Pipelines

- A pipeline consists of stages (build, test, deploy) and jobs within them.
- Jobs specify the tasks to be performed in each stage. For example, a job can compile or test code.
- Pipelines trigger on commits, merges, or scheduled events.

### Use CI/CD Variables

- Store configuration settings and secrets (e.g., API keys).
- Two types: Custom variables (user-defined) and Predefined variables (automatically set by GitLab).
- Can be protected (restricted to certain branches) or masked (hidden in logs).

### Utilize CI/CD Components

- Reusable pipeline configurations to reduce duplication and maintain consistency.
- Can be included in a pipeline via include:component.
- GitLab provides prebuilt templates for common tasks.

## yaml example

```bash
build-job:
  stage: build
  script:
    - echo "Hello, $GITLAB_USER_LOGIN!"

test-job1:
  stage: test
  script:
    - echo "This job tests something"

test-job2:
  stage: test
  script:
    - echo "This job tests something, but takes more time than test-job1."
    - echo "After the echo commands complete, it runs the sleep command for 20 seconds"
    - echo "which simulates a test that runs 20 seconds longer than test-job1"
    - sleep 20

deploy-prod:
  stage: deploy
  script:
    - echo "This job deploys something from the $CI_COMMIT_BRANCH branch."
  environment: production
```


## Artifacts reports

Use ```artifacts:reports``` to:

- collect test reports, code quality reports, security reports and others.
- This reports are used to display information in merge requests, pipeline views and security dashboards.

This reports are always uploaded, regardless of the job results. Use ```artifacts:expire_in``` to set an expiration time.

To browse the report output files, include ```artifacts:paths``` in the job definition.

There is a lot of type of artifacts, so here are the most used. For more information about other types of artifacts [see official documentation](https://docs.gitlab.com/ci/yaml/artifacts_reports/).

### ```artifacts:reports:junit```

This type of artifacts allow to save 

```bash
  artifacts:
    when: always
    reports:
      junit: /app/tests/results.xml
    expire_in: "5 days"
```