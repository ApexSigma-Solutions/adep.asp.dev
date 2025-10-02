# Python SDK

{% hint style="success" %}
<img src="https://img.shields.io/pypi/v/arize?label=pypi%20latest&#x26;color=dark-green" alt="PyPI - Version" data-size="original"> ![PyPI - Status](https://img.shields.io/pypi/status/arize) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/arize?logo=python\&logoColor=green)
{% endhint %}

Use the Arize Python package to create datasets, run experiments, get traces, and log evaluations to Arize. You can also use our ML features to log predictions and actuals. See our API reference below.

{% embed url="https://arize-client-python.readthedocs.io/en/latest/" %}

## Installing the package <a href="#installing-the-package" id="installing-the-package"></a>

```bash
pip install arize
```

## Changelog

The Arize SDK has additional functionality that can be installed with extra dependencies:

{% embed url="https://github.com/Arize-ai/client_python/blob/main/CHANGELOG.md" %}

## End of Support Table

<table data-full-width="false"><thead><tr><th width="160">Major Release</th><th>First Released</th><th width="135">Latest</th><th>Support</th></tr></thead><tbody><tr><td>7.x</td><td>June, 2023</td><td><a href="https://pypi.org/project/arize/">latest</a></td><td><mark style="background-color:green;">Ends June 1st, 2026</mark></td></tr><tr><td>6.x</td><td>January, 2023</td><td>6.1.3</td><td><mark style="background-color:green;">Ends June 1st, 2025</mark></td></tr><tr><td>5.x</td><td>August, 2022</td><td>5.5.0</td><td><mark style="background-color:red;">Ends November 1st, 2024</mark></td></tr><tr><td>4.x</td><td>March, 2022</td><td>4.2.2</td><td><mark style="background-color:red;">Ended June 1st, 2024</mark></td></tr><tr><td>3.x</td><td>September, 2021</td><td>3.4.0</td><td><mark style="background-color:red;">Ended April 1st, 2024</mark></td></tr><tr><td>2.x</td><td>March, 2021</td><td>2.2.1</td><td><mark style="background-color:red;">Ended July 1st, 2023</mark></td></tr><tr><td>1.x</td><td>July, 2020</td><td>1.2.1</td><td><mark style="background-color:red;">Ended March 1st, 2022</mark></td></tr><tr><td>0.x</td><td>March, 2020</td><td>0.0.20</td><td><mark style="background-color:red;">Ended March 1st, 2022</mark></td></tr></tbody></table>

## Available packages

The main package is arize, and you can add additional functionality by adding extra dependencies. ![python>=3.8](https://img.shields.io/badge/python-3_8-red) is the minimum required for the additional packages.

<table><thead><tr><th width="235.7603759765625">Package</th><th>What It's For</th></tr></thead><tbody><tr><td>arize</td><td>The primary Arize package for interfacing with Arize APIs.</td></tr><tr><td><a href="https://app.gitbook.com/s/-MAlgpMyBRcl2qFZRQ67/observe/tracing">arize[Tracing]</a></td><td>Components for logging traces and running experiments for LLM applications.</td></tr><tr><td><a href="https://app.gitbook.com/s/-MAlgpMyBRcl2qFZRQ67/machine-learning/machine-learning/api-reference-ml/python-sdk/arize.pandas/autoembeddings">arize[AutoEmbeddings]</a></td><td>Automatically generate embeddings vectors for your predictions and actuals for ML models.</td></tr><tr><td><a href="https://app.gitbook.com/s/-MAlgpMyBRcl2qFZRQ67/machine-learning/machine-learning/api-reference-ml/python-sdk/arize.pandas/llm_evaluation">arize[NLP_Metrics]</a></td><td>Calculate evaluation metrics for your NLP Generative tasks. </td></tr><tr><td><a href="https://app.gitbook.com/s/-MAlgpMyBRcl2qFZRQ67/machine-learning/machine-learning/how-to-ml/explainability">arize[MimicExplainer]</a></td><td>Produce SHAP values using the surrogate explainability approach. </td></tr></tbody></table>
