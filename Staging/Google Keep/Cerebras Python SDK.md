---
tags:
  - Keep/Label/AI-Tools
  - Keep/Label/Python
  - Keep/Label/ApexSigma-Solutions
---

https://cloud.cerebras.ai/platform/org_mfrn2h8rkv3trwf6hc35xypf/playground

import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    # This is the default and can be omitted
    api_key=os.environ.get("CEREBRAS_API_KEY")
)

stream = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": ""
        }
    ],
    model="gpt-oss-120b",
    stream=True,
    max_completion_tokens=65536,
    temperature=1,
    top_p=1,
    reasoning_effort="medium"
)

for chunk in stream:
  print(chunk.choices[0].delta.content or "", end="")