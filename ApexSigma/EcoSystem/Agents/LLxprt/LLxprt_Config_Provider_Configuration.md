# LLxprt Config Provider Configuration

````
## Using OpenAI
Direct access to o3, o1, GPT-4.1, and other OpenAI models:

Get your API key from OpenAI
Configure LLxprt Code:

```
/provider openai
/key sk-your-openai-key-here
/model o3-mini
```

## Using Anthropic
Access Claude Sonnet 4, Claude Opus 4.1, and other Anthropic models:

Option 1: Log in with Anthropic to use your Claude Pro or Max account

### Use OAuth authentication to access Claude with your existing Claude Pro or Max subscription:

Select the Anthropic provider:

```
/provider anthropic
```
### Authenticate with your Claude account:

```
/auth
```

Your browser will open to the Claude authentication page

Log in and authorize LLxprt Code

Copy the authorization code shown and paste it back in the terminal
You're now using your Claude Pro/Max account!

### Option 2: Use an API Key

Get your API key from Anthropic

Configure:

````
```
/provider anthropic

/key sk-ant-your-key-here

/model claude-sonnet-4-20250115
```

## Using Qwen
Access Qwen3-Coder-Pro and other Qwen models for free:

### Option 1: Log in with Qwen (FREE)
Use OAuth authentication to access Qwen with your free account:

```
/auth qwen enable
```

This enables OAuth for Qwen. When you send your first message, your browser will automatically open to the Qwen authentication page. Log in and authorize LLxprt Code - the authentication will complete automatically and your request will be processed. You're now using Qwen3-Coder-Pro for free!

### Option 2: Use an API Key

For advanced users who need API access:

Get your API key from Qwen
Configure:

```
/provider qwen
/key your-qwen-api-key
/model qwen3-coder-pro
```

## Using Cerebras Code Max/Pro

Access Cerebras Code Max/Pro plan with the powerful qwen-3-coder-480b model

Get your API key from Cerebras

Configure LLxprt Code:

```
/provider openai
/baseurl https://api.cerebras.ai/v1
/key your-cerebras-api-key
/model qwen-3-coder-480b
```

For optimal performance with this model, consider setting a high context limit:

```
/set context-limit 100000
```

## Using Local Models

Run models locally for complete privacy and control. LLxprt Code works with any OpenAI-compatible server.

Example with LM Studio:

Start LM Studio and load a model (e.g., Gemma 3B)
In LLxprt Code:

```
/provider openai
/baseurl http://127.0.0.1:1234/v1/
/model gemma-3b-it
```

Example with llama.cpp:

Start llama.cpp server: 

```
./server -m model.gguf -c 2048
```

In LLxprt Code:

```
/provider openai
/baseurl http://localhost:8080/v1/
/model local-model
```

List available models:

```
/model
```

This shows all models available from your current provider.

## Using OpenRouter

Access 100+ models through OpenRouter:

Get your API key from OpenRouter
Configure LLxprt Code:

```
/provider openai
/baseurl https://openrouter.ai/api/v1/
/keyfile ~/.openrouter_key
/model qwen/qwen3-coder
/profile save qwen3-coder
```

## Using Fireworks

For fast inference with popular open models:

Get your API key from Fireworks
Configure:

```
/provider openai
/baseurl https://api.fireworks.ai/inference/v1/
/key fw_your-key-here
/model accounts/fireworks/models/llama-v3p3-70b-instruct
```

## Using xAI (Grok)
Access Grok models through xAI's API:

Get your API key from xAI

Configure using command line:

```
llxprt --provider openai --baseurl https://api.x.ai/v1/ --model grok-3 --keyfile ~/.mh_key
```

Or configure interactively:

```
/provider openai
/baseurl https://api.x.ai/v1/
/model grok-3
/keyfile ~/.mh_key
```

List available Grok models:

```
/model
```

## Using Google Gemini

You can still use Google's services:

With Google Account: Use /auth to sign in
With API Key:

export GEMINI_API_KEY="YOUR_API_KEY"

Or 

use /key YOUR_API_KEY after selecting the gemini provider
Managing API Keys

Set key for current session: /key your-api-key
Load key from file: /keyfile ~/.keys/openai.txt
Environment variables: Still supported for all providers

````