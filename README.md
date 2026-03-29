# cc-provider-switcher

Hermes-agent plugin that lets you run Claude Code with alternative LLM providers (GLM, Kimi, MiniMax, etc.) via environment variable switching.

## Installation

```bash
hermes plugins install tmdgusya/cc-provider-switcher
```

Or manually:

```bash
git clone https://github.com/tmdgusya/cc-provider-switcher.git \
  ~/.hermes/plugins/cc-provider-switcher
```

Restart Hermes after installation.

## Configuration

Edit `~/.hermes/plugins/cc-provider-switcher/config.yaml`:

```yaml
# Subprocess timeout in seconds (default: 600)
timeout: 600

# Add custom providers beyond the built-in ones
custom_providers:
  deepseek:
    name: "DeepSeek"
    slug: "deepseek"
    base_url_env: "GT_DEEPSEEK_BASE_URL"
    auth_token_env: "GT_DEEPSEEK_AUTH_TOKEN"
    base_url_default: "https://api.deepseek.com/anthropic"
    default_model_default: "deepseek-r1"
    emoji: "🔵"
    description: "DeepSeek models via Anthropic-compatible proxy"
```

Set the required environment variables for your provider:

```bash
# Example: GLM
export GT_GLM_AUTH_TOKEN="your-api-key"

# Example: Kimi
export GT_KIMI_AUTH_TOKEN="your-api-key"
```

## Built-in Providers

| Provider | Slug | Env Vars |
|----------|------|----------|
| GLM (Z.ai) | `glm` | `GT_GLM_BASE_URL`, `GT_GLM_AUTH_TOKEN` |
| Kimi (Moonshot) | `kimi` | `GT_KIMI_BASE_URL`, `GT_KIMI_AUTH_TOKEN` |
| MiniMax | `minimax` | `GT_MINIMAX_BASE_URL`, `GT_MINIMAX_AUTH_TOKEN` |
| Claude (native) | `claude` | Uses default Claude Code config |

## Tools

- **`provider_claude_code`** — Run Claude Code with a specific provider
- **`provider_list`** — List available providers and their status

## Usage

In Hermes, the model can call these tools directly:

```
Use GLM to refactor the auth module
```

Or check available providers:

```
List available LLM providers
```

## License

MIT
