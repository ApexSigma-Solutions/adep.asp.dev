---
tags:
  - ApexSigma
  - pytest
  - trunk
  - Flaky
---
# Pytest

You can automatically [detect and manage flaky tests](https://docs.trunk.io/flaky-tests/detection) in your Pytest projects by integrating with Trunk. This document explains how to configure Pytest to output JUnit XML reports that can be uploaded to Trunk for analysis.

### Checklist

By the end of this guide, you should achieve the following before proceeding to the [next steps](#next-step) to configure your CI provider.

* [ ] Generate a compatible test report
* [ ] Configure the report file path or glob
* [ ] Disable retries for better detection accuracy
* [ ] Test uploads locally

After correctly generating reports following the above steps, you'll be ready to move on to the next steps to [configure uploads in CI](https://docs.trunk.io/flaky-tests/get-started/ci-providers).

### Generating Reports

Trunk detects flaky tests by analyzing test reports automatically uploaded from your CI jobs. You can do this by generating JUnit XML reports from your test runs.

In your CI job, update your `pytest` command to include the `--junit-xml` and `junit_family=xunit1` arguments to generate XML reports:

```shell
pytest --junit-xml=junit.xml -o junit_family=xunit1
```

The `junit_family=xunit1` is necessary so that the generated XML report includes file paths for each test case. File paths for test cases are used for features that use code owners like the [Jira integration](https://docs.trunk.io/flaky-tests/ticketing-integrations/jira-integration) and [webhooks](https://docs.trunk.io/flaky-tests/webhooks).

#### Report File Path

The `--junit-xml` argument specifies the path of the JUnit report. You'll need this path later when configuring automatic uploads to Trunk.

#### Disable Retries

You need to disable automatic retries if you previously enabled them. Retries compromise the accurate detection of flaky tests. You should disable retries for accurate detection and use the [Quarantining](https://docs.trunk.io/flaky-tests/quarantining) feature to stop flaky tests from failing your CI jobs.

Omit the [`--lf` or `--ff` options](https://docs.pytest.org/en/stable/how-to/cache.html) if you've previously configured your CI with these options to disable retries.

### Try It Locally

You can validate your test reports using the [Trunk CLI](https://docs.trunk.io/flaky-tests/uploader). If you don't have it installed already, you can install and run the `validate` command like this:

```sh
curl -fsSLO --retry 3 https://trunk.io/releases/trunk && chmod +x trunk
./trunk flakytests validate --junit-paths "./junit.xml"
```

**This will not upload anything to Trunk**. To improve detection accuracy, you should **address all errors and warnings** before proceeding to the next steps.

#### **The Validate Command**

You can validate your test reports using the [Trunk CLI](https://docs.trunk.io/flaky-tests/uploader). If you don't have it installed already, you can install and run the `validate` command like this:

```sh
curl -fsSLO --retry 3 https://trunk.io/releases/trunk && chmod +x trunk
./trunk flakytests validate --junit-paths "./junit.xml"
```

**This will not upload anything to Trunk**. To improve detection accuracy, you should **address all errors and warnings** before proceeding to the next steps.

#### Test Upload

Before modifying your CI jobs to automatically upload test results to Trunk, try uploading a single test run manually.

You make an upload to Trunk using the following command:

```sh
curl -fsSLO --retry 3 https://trunk.io/releases/trunk && chmod +x trunk
./trunk flakytests upload --junit-paths "./junit.xml" \
    --org-url-slug <TRUNK_ORG_SLUG> \
    --token <TRUNK_ORG_TOKEN>
```

You can find your Trunk organization slug and token in the settings or by following these [instructions](https://docs.trunk.io/flaky-tests/get-started/ci-providers/otherci#id-1.-store-a-trunk_token-secret-in-your-ci-system). After your upload, you can verify that Trunk has received and processed it successfully in the **Uploads** tab. Warnings will be displayed if the report has issues.

<figure><picture><source srcset="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2Fg864QZiiLiLUkXC3sEe4%2Fdata-uploads-dark.png?alt=media&#x26;token=6debdbd5-91fe-4dc2-8ff3-1edb9e69d7b2" media="(prefers-color-scheme: dark)"><img src="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FiUbhiEbyfkIHQZ60zgS9%2Fdata-uploads-light.png?alt=media&#x26;token=937efcaa-1516-4686-a434-3570bc9ea802" alt=""></picture><figcaption></figcaption></figure>

### Next Steps

Configure your CI to upload test runs to Trunk. Find the guides for your CI framework below:

<table data-view="cards" data-full-width="false"><thead><tr><th></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><strong>Azure DevOps Pipelines</strong></td><td></td><td><a href="../ci-providers/azure-devops-pipelines">azure-devops-pipelines</a></td><td><a href="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FQ0rWUH25QyqS5GDS55lT%2Fazure.png?alt=media&#x26;token=8c1f9384-193c-4c9a-b112-f5561613f4eb">azure.png</a></td></tr><tr><td><strong>BitBucket Pipelines</strong></td><td></td><td><a href="../ci-providers/bitbucket-pipelines">bitbucket-pipelines</a></td><td><a href="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FabnU59zhrjW2NHoPDfvi%2Fbitbucket.png?alt=media&#x26;token=57c3f77d-ec25-4379-911e-4fbc3c598307">bitbucket.png</a></td></tr><tr><td><strong>BuildKite</strong></td><td></td><td><a href="../ci-providers/buildkite">buildkite</a></td><td><a href="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FNcUukSy7Akhwp1gY95KM%2Fbuildkite.png?alt=media&#x26;token=e9f76b00-59f8-40cd-b36b-91a5f4346425">buildkite.png</a></td></tr><tr><td><strong>CircleCI</strong></td><td></td><td><a href="../ci-providers/circleci">circleci</a></td><td><a href="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FtNKP5xVE83n9ANPQNRui%2Fcircle-ci.png?alt=media&#x26;token=572bfc49-0f46-4da7-a5a0-b8a6532b5116">circle-ci.png</a></td></tr><tr><td><strong>Drone CI</strong></td><td></td><td><a href="../ci-providers/droneci">droneci</a></td><td><a href="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FT5SjdSpdr0bUe7QyKEA7%2Fdrone.png?alt=media&#x26;token=bcd35586-c5d8-4101-9a7e-b14a91df74ed">drone.png</a></td></tr><tr><td><strong>GitHub Actions</strong></td><td></td><td><a href="../ci-providers/github-actions">github-actions</a></td><td><a href="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FQ9mNmLONCxyxAPARPoo5%2Fgithub.png?alt=media&#x26;token=b5ca383b-e0d4-4a2c-84df-8e5b248089f0">github.png</a></td></tr><tr><td><strong>Gitlab</strong></td><td></td><td><a href="../ci-providers/gitlab">gitlab</a></td><td><a href="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FxvmPC1rebwt2t3mf3eiu%2Fgitlab.png?alt=media&#x26;token=c596a5e4-5a1a-49f6-a85a-6344bc52bf17">gitlab.png</a></td></tr><tr><td><strong>Jenkins</strong></td><td></td><td><a href="../ci-providers/jenkins">jenkins</a></td><td><a href="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FVMm9Exm5TBYCAYafWa1N%2Fjenkins.png?alt=media&#x26;token=7243f37d-9fa4-47d7-a9f8-9d871bdde7e3">jenkins.png</a></td></tr><tr><td><strong>Semaphore</strong></td><td></td><td><a href="../ci-providers/semaphoreci">semaphoreci</a></td><td><a href="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FbdwX7ZvV4PygwxSKI9Z7%2Fsemaphore.png?alt=media&#x26;token=bc70d20a-5971-42a2-b53a-18a3bd889589">semaphore.png</a></td></tr><tr><td><strong>TeamCity</strong></td><td></td><td><a href="https://github.com/trunk-io/docs/blob/main/flaky-tests/get-started/frameworks/broken-reference/README.md">https://github.com/trunk-io/docs/blob/main/flaky-tests/get-started/frameworks/broken-reference/README.md</a></td><td><a href="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FMpdPtpzMnqKRiBWVNgtm%2Fteamcity.png?alt=media&#x26;token=5b095409-4374-4e70-91bf-0eff9ec3386b">teamcity.png</a></td></tr><tr><td><strong>Travis CI</strong></td><td></td><td><a href="../ci-providers/travisci">travisci</a></td><td><a href="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FUCPJObs9AQFQELbc8OHC%2Ftravis.png?alt=media&#x26;token=cdea623e-aac9-4ec5-bf66-991e525dfe13">travis.png</a></td></tr><tr><td><strong>Other CI Providers</strong></td><td></td><td><a href="../ci-providers/otherci">otherci</a></td><td><a href="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FzvwIJ7OxPKzabAuIFAwD%2Fother.png?alt=media&#x26;token=705898fa-ceb4-4972-88e6-9b2be5dcd002">other.png</a></td></tr></tbody></table>