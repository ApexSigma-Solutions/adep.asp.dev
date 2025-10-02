## Keys

```env

XAI_API_KEY = 'xai-iRSUa7HlRSNdoot6luO5EZsR0v2kYKqZSSsLubXDNLMzmcjq2s8saO0Y27XrJvQUIhYJ66RHXyPPlrPV'


XAI_API_KEY_ = 'xai-WX2d1YiCm4VLl7yxLU6wEqEqW3aame56D7hlhGIJmuP4qpNmKuyFtHLdENpj2oFKx8EPWAGeyo3zPEmp'
```

## Completions

```shell
curl https://api.x.ai/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer xai-WX2d1YiCm4VLl7yxLU6wEqEqW3aame56D7hlhGIJmuP4qpNmKuyFtHLdENpj2oFKx8EPWAGeyo3zPEmp" \
    -d '{
      "messages": [
        {
          "role": "system",
          "content": "You are a test assistant."
        },
        {
          "role": "user",
          "content": "Testing. Just say hi and hello world and nothing else."
        }
      ],
      "model": "grok-4-latest",
      "stream": false,
      "temperature": 0
    }'
```

```shell
curl https://api.x.ai/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer xai-WX2d1YiCm4VLl7yxLU6wEqEqW3aame56D7hlhGIJmuP4qpNmKuyFtHLdENpj2oFKx8EPWAGeyo3zPEmp" \
    -d '{
      "messages": [
        {
          "role": "system",
          "content": "You are a test assistant."
        },
        {
          "role": "user",
          "content": "Testing. Just say hi and hello world and nothing else."
        }
      ],
      "model": "grok-4-latest",
      "stream": false,
      "temperature": 0
    }'
```

[[LLxprt_Config_Provider_Configuration]]