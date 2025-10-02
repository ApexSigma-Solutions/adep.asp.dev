---
aliaes: Trunk Analysis
title: Trunk Analytics CLI Reference
tags:
  - ApexSigma
  - CLI
  - Analytics
  - trunk
---
# Trunk Analytics CLI Reference

Trunk detects and tracks flaky tests in your repos by receiving uploads from your test runs in CI, uploaded from the Trunk Analytics CLI. These uploads happen in the CI jobs used to run tests in your nightly CI, post-commit jobs, and PR checks.&#x20;

### Guides

If you're setting up Trunk Flaky Tests for the first time, you can follow the guides for your CI provider and test framework.

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th data-hidden></th><th data-hidden></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Guides by Test Frameworks</td><td></td><td></td><td><a href="get-started/frameworks">frameworks</a></td></tr><tr><td>Guides by CI Provider</td><td></td><td></td><td><a href="get-started/ci-providers">ci-providers</a></td></tr></tbody></table>

### Using Unsupported CI Systems

The CLI is preconfigured to work with a set [ci-providers](https://docs.trunk.io/flaky-tests/get-started/ci-providers "mention") and can be used with other systems by setting up and passing [#environment-variables](https://docs.trunk.io/get-started/ci-providers/otherci#environment-variables "mention")  to the uploader.&#x20;

> More information on using [otherci](https://docs.trunk.io/flaky-tests/get-started/ci-providers/otherci "mention") is documented here.

### Installing the CLI

The CLI should be **downloaded as part of your test workflow** in your CI system. The launcher is platform agnostic and will download the latest version of the uploader for your platform.&#x20;

{% hint style="success" %}
You should **always use the latest version** of the Trunk Analytics CLI by downloading it fresh in your CI jobs for the best detection results.
{% endhint %}

You can download the Trunk Analytics CLI and mark it executable with the following command:

```bash
curl -fsSLO --retry 3 https://trunk.io/releases/trunk && chmod +x trunk
```

And you can verify that it's been downloaded properly by running:

```sh
./trunk flakytests -V
```

Under-the-hood, this downloads the [Trunk CLI Launcher](https://docs.trunk.io/references/cli/install#the-trunk-launcher) which will download the appropriate binaries for your environment.&#x20;

### Organization Slug and Token

The CLI requires your Trunk organization slug and token passed through `--org-url-slug` and `--token` to upload results to the correct organzation.&#x20;

You can find your organization slug and token by going to **Settings** > **Manage** > **Organization**.&#x20;

{% tabs %}
{% tab title="Slug" %}

<figure><picture><source srcset="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2Fc5tUoWpZjDrSOKyZ9DU3%2Forg-slug-dark.png?alt=media&#x26;token=fab7849a-b967-4a68-a37c-9b31c9416f19" media="(prefers-color-scheme: dark)"><img src="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2Fv3r98mawuLqv0JBkOM26%2Forg-slug-light.png?alt=media&#x26;token=2bf29526-7030-481a-ba1d-0968bd3cd939" alt=""></picture><figcaption><p>Make sure you are getting your <em>Organization Slug</em>, not the Organization Name.</p></figcaption></figure>
{% endtab %}

{% tab title="Token" %}

<figure><picture><source srcset="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FODVCmzwXQvdTKzwpCH2L%2Forg-token-dark.png?alt=media&#x26;token=3ccb3715-011a-412f-bd41-67840e7a7c2e" media="(prefers-color-scheme: dark)"><img src="https://577236045-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F61Ep9MrYBkJa0Yq3zS1s%2Fuploads%2FPHvJn2OosdPzZDZ5hFMg%2Forg-token-light.png?alt=media&#x26;token=ab8d0415-148b-4efb-9cbb-32344dd9bc71" alt=""></picture><figcaption><p>Ensure you get your <em>Organization API Token</em>, <em><strong>not your repo token</strong></em>.</p></figcaption></figure>

{% endtab %}
{% endtabs %}

### Uploading Using the CLI

{% hint style="info" %}
The uploaded tests are processed by Trunk periodically, not in real-time. Wait for at least an hour after the initial upload before they’re displayed in the [Uploads tab](https://docs.trunk.io/get-started#id-4.-confirm-your-configuration-analyze-your-dashboard). Multiple uploads are required before a test can be accurately detected as broken or flaky.
{% endhint %}

Trunk accepts uploads in three main report formats, [XML](https://github.com/testmoapp/junitxml), [Bazel Event Protocol JSONs](https://bazel.build/remote/bep#consuming-bep-text-json), and XCode XCResult paths. You can upload each of these test report formats using the `./trunk flakytest upload` command like this:

{% tabs %}
{% tab title="XML" %}
Trunk can accept JUnit XMLs through the `--junit-paths` argument:

```
./trunk flakytests upload --junit-paths "test_output.xml" \
   --org-url-slug <TRUNK_ORG_SLUG> \
   --token $TRUNK_API_TOKEN
```

{% endtab %}

{% tab title="Bazel" %}
Trunk can accept Bazel through the `--bazel-bep-path` argument:

```
./trunk flakytests upload --bazel-bep-path <BEP_JSON_PATH> \
   --org-url-slug <TRUNK_ORG_SLUG> \
   --token $TRUNK_API_TOKEN
```

{% endtab %}

{% tab title="XCode" %}
Trunk can accept XCode through the `--xcresult-path` argument:

```
./trunk flakytests upload --xcresult-path <XCRESULT_PATH> \
   --org-url-slug <TRUNK_ORG_SLUG> \
   --token $TRUNK_API_TOKEN
```

{% endtab %}
{% endtabs %}

### Testing Using the CLI

You can also execute tests and upload results to Trunk in a single step using the `./trunk flakytest test` command to **wrap** your test command.&#x20;

This is especially useful for [Quarantining](https://docs.trunk.io/flaky-tests/quarantining), where the Trunk CLI will **override the exit code** of the test command if all failures can be quarantined, **preventing** flaky tests from failing your builds in CI.

{% tabs %}
{% tab title="XML" %}
Trunk can accept JUnit XMLs through the `--junit-paths` argument:

```
./trunk flakytests test --junit-paths "test_output.xml" \
   --org-url-slug <TRUNK_ORG_SLUG> \
   --token $TRUNK_API_TOKEN \
   <YOUR_TEST_COMMAND>
```

{% endtab %}

{% tab title="Bazel" %}
Trunk can accept Bazel through the `--bazel-bep-path` argument:

```
./trunk flakytests test --bazel-bep-path <BEP_JSON_PATH> \
   --org-url-slug <TRUNK_ORG_SLUG> \
   --token $TRUNK_API_TOKEN \
   <YOUR_TEST_COMMAND>
```

{% endtab %}

{% tab title="XCode" %}
Trunk can accept XCode through the `--xcresult-path` argument:

```
./trunk flakytests test --xcresult-path <XCRESULT_PATH> \
   --org-url-slug <TRUNK_ORG_SLUG> \
   --token $TRUNK_API_TOKEN \
   <YOUR_TEST_COMMAND>
```

{% endtab %}
{% endtabs %}

#### Upload failure vs test failure

We use the `SOFTWARE` exit code (70) if the upload fails.

If you use the `test` command and tests fail without the failures being quarantined, we return the provided exit code from the wrapped execution.

If you use the `upload` command, we return exit code `FAILURE` or the exit code provided with the `--test_process_exit_code` argument.

### Validating Reports Locally

You can validate the test reports produced by your test frameworks before you set up Trunk in your CI jobs. This is currently **only available for XML reports**.

You can run the validate command like this:

```
./trunk flakytests validate --junit-paths "test_output.xml"
```

The `./trunk flakytests validate` command will output any problems with your reports so you can address them before setting up Trunk in CI.

```sh
Validating the following 1 files:
  File set matching junit.xml:
    junit.xml

junit.xml - 1 test suites, 0 test cases, 0 validation errors

All 1 files are valid! ✅
Navigate to https://app.trunk.io/onboarding?intent=flaky+tests to continue using Trunk Flaky Tests! 🚀🧪
```

### Upgrade

If you installed the CLI in your CI jobs following the instructions in the [Installing the CLI step](Trunk%20Analytics%20CLI%20Reference.md), the CI job will automatically install the latest version of the CLI. You should **always download a fresh copy of the latest CLI in CI**.

If you're using the `flakytests` CLI subcommand with the Trunk CLI locally, you can upgrade with this command:

<pre class="language-bash"><code class="lang-bash"><strong>./trunk flakytests --upgrade
</strong></code></pre>

### Full Command Reference

The `trunk` command-line tool can upload and analyze test results. The `trunk flakytests` command accepts the following subcommands:

| Command                           | Description                                                                                                                                                                                                            |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `trunk flakytests upload`         | Upload data to Trunk Flaky Tests.                                                                                                                                                                                      |
| `trunk flakytests validate`       | Validates if the provided JUnit XML files and prints any errors.                                                                                                                                                       |
| `trunk flakytests test <COMMAND>` | Runs tests using the provided command, uploads results, checks whether the failures are [quarantined](https://docs.trunk.io/quarantining#using-the-trunk-cli-directly) tests, and correct the exit code based on that. |

The `upload` and `test` commands accept the following options:

<table><thead><tr><th width="265">Argument</th><th>Description</th></tr></thead><tbody><tr><td><code>--junit-paths &#x3C;JUNIT_PATHS></code></td><td>Path to the test output files. File globs are supported. Remember to wrap globs in <code>""</code> quotes</td></tr><tr><td><code>--bazel-bep-path &#x3C;BEP_JSON_PATH></code></td><td>Path to a JSON serialized <a href="https://bazel.build/remote/bep">Bazel Build Event Protocol</a>. Trunk will use the BEP file to locate test reports. Your test frameworks must still output <a href="get-started/frameworks">compatible report formats</a>.</td></tr><tr><td><code>--xcresult-path &#x3C;XCRESULT_PATH></code></td><td>Path to a <code>.xcresult</code> directory, which contains test reports from <code>xcodebuild</code>.</td></tr><tr><td><code>--org-url-slug &#x3C;ORG_URL_SLUG></code></td><td>Trunk Organization slug, from the Settings page.</td></tr><tr><td><code>--token &#x3C;TOKEN></code></td><td>Trunk Organization (not repo) token, from the Settings page. Defaults to the <code>TRUNK_API_TOKEN</code> variable.</td></tr><tr><td><code>-h, --help</code></td><td>Additional detailed description of the <code>upload</code> command.</td></tr><tr><td><code>--repo-root</code></td><td>Path to the repository root. Defaults to the current directory.</td></tr><tr><td><code>--repo-url &#x3C;REPO_URL></code></td><td>Value to override URL of repository. <strong>Optional</strong>.</td></tr><tr><td><code>--repo-head-sha</code> <code>&#x3C;REPO_HEAD_SHA></code></td><td>Value to override SHA of repository head. <strong>Optional</strong>.</td></tr><tr><td><code>--repo-head-branch &#x3C;REPO_HEAD_BRANCH></code></td><td>Value to override branch of repository head. <strong>Optional</strong>.</td></tr><tr><td><code>--repo-head-commit-epoch &#x3C;REPO_HEAD_COMMIT_EPOCH></code></td><td>Value to override commit epoch of repository head. <strong>Optional</strong>.</td></tr><tr><td><code>--codeowners-path &#x3C;CODEOWNERS_PATH></code></td><td>Value to override CODEOWNERS file or directory path. <strong>Optional</strong>.</td></tr><tr><td><code>--allow-empty-test-results</code></td><td>Don't fail commands if test results are empty or missing. Use it when you sometimes skip all tests for certain CI jobs. Defaults to <code>true</code>.</td></tr><tr><td><code>--variant &#x3C;VARIANT_NAME></code></td><td>Upload tests to a specific variant group. <strong>Optional</strong>.</td></tr><tr><td><code>--test-process-exit-code</code> <code>&#x3C;EXIT_CODE></code></td><td>Specify the exit code of the test previously run. This is used by the upload command to identify errors that happen outside of the context of the test execution (such as build errors).</td></tr></tbody></table>

[[The Trunk Launcher]]
[[Code Quality with Trunk]]
[[Pytest with Trunk]]
