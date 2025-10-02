### **The Validate Command**

You can validate your test reports using the [Trunk CLI](https://app.trunk.io/flaky-tests/uploader.md). If you don't have it installed already, you can install and run the validate command like this:

curl -fsSLO --retry 3 https://trunk.io/releases/trunk && chmod +x trunk
./trunk flakytests validate --junit-paths "./junit.xml"

**This will not upload anything to Trunk**. To improve detection accuracy, you should **address all errors and warnings** before proceeding to the next steps.

### Test Upload

Before modifying your CI jobs to automatically upload test results to Trunk, try uploading a single test run manually.

You make an upload to Trunk using the following command:

curl -fsSLO --retry 3 https://trunk.io/releases/trunk && chmod +x trunk
./trunk flakytests upload --junit-paths "./junit.xml" \
    --org-url-slug apexsigma-solutions \
    --token jT8ICR4omEZfY0MghvjGH58oq6TCbP3o2uXJSJ06

You can find your Trunk organization slug and token in the settings or by following these [instructions](https://docs.trunk.io/flaky-tests/get-started/ci-providers/otherci#id-1.-store-a-trunk_token-secret-in-your-ci-system). After your upload, you can verify that Trunk has received and processed it successfully in the **Uploads** tab. Warnings will be displayed if the report has issues.