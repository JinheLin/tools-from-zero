```
export ANTHROPIC_BASE_URL="https://code.newcli.com/claude/aws"
export ANTHROPIC_AUTH_TOKEN="替换为您的API Key"

claude --model claude-opus-4-6

claude-opus-4-5-thinking

claude-opus-4-5
```



```
codex -p xx -m xx
```



```toml
personality = "pragmatic"
model_provider = "bk"
model = "gpt-5.3-codex"
model_reasoning_effort = "xhigh"

disable_response_storage = true
approval_policy = "never"
sandbox_mode = "danger-full-access"
use_git = true

[model_providers.right]
name = "right"
base_url = "https://right.codes/codex/v1"
wire_api = "responses"
requires_openai_auth = true
env_key = "RIGHT_KEY"

[model_providers.bk]
name = "bk"
base_url = "https://free.xxsxx.fun/v1"
wire_api = "responses"
requires_openai_auth = true
env_key = "BK_KEY"

[model_providers.fox]
name = "fox"
base_url = "https://code.newcli.com/codex/v1"
wire_api = "responses"
requires_openai_auth = true
env_key = "FOX_KEY"

[shell_environment_policy]
inherit = "all"

[features]
git = true
search = true

```

