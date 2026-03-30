"""Tool handlers for provider-switcher plugin."""

from __future__ import annotations

import json
import logging
import os
import subprocess
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Module-level ref set by __init__.py
_config: Dict[str, Any] = {}


_PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))


def _find_clean_claude_binary() -> str:
    """Locate the clean-claude wrapper script."""
    wrapper = os.path.join(_PLUGIN_DIR, "bin", "clean-claude")
    if os.path.isfile(wrapper) and os.access(wrapper, os.X_OK):
        return wrapper
    raise FileNotFoundError(
        f"clean-claude wrapper not found at {wrapper}"
    )


def handle_provider_claude_code(args: dict, **kwargs) -> str:
    """Run Claude Code with the specified provider's environment."""
    try:
        provider = args.get("provider", "claude")
        prompt = args.get("prompt", "")
        workdir = args.get("workdir", os.getcwd())
        skip_perms = args.get("dangerously_skip_permissions", True)

        if not prompt:
            return json.dumps({"error": "prompt is required"})

        # Build command using clean-claude wrapper
        clean_claude = _find_clean_claude_binary()
        cmd = [clean_claude, "--provider", provider]
        if skip_perms:
            cmd.append("--dangerously-skip-permissions")
        cmd.extend(["-p", prompt])

        # Expand workdir
        workdir = os.path.expanduser(workdir)
        if not os.path.isdir(workdir):
            return json.dumps({"error": f"workdir does not exist: {workdir}"})

        timeout = _config.get("timeout", 600)

        logger.info(
            "Running Claude Code with provider=%s workdir=%s timeout=%ds",
            provider, workdir, timeout,
        )

        result = subprocess.run(
            cmd,
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        output = result.stdout
        if result.stderr:
            output += "\n\n[stderr]\n" + result.stderr

        # Truncate very long outputs
        max_len = 100_000
        if len(output) > max_len:
            output = output[:max_len] + f"\n\n[truncated at {max_len} chars]"

        return json.dumps({
            "provider": provider,
            "exit_code": result.returncode,
            "output": output,
        })

    except subprocess.TimeoutExpired:
        return json.dumps({
            "error": f"Claude Code timed out after {_config.get('timeout', 600)}s",
            "provider": args.get("provider", "unknown"),
        })
    except ValueError as exc:
        return json.dumps({"error": str(exc)})
    except FileNotFoundError as exc:
        return json.dumps({"error": str(exc)})
    except Exception as exc:
        logger.exception("provider_claude_code failed")
        return json.dumps({"error": f"Unexpected error: {exc}"})


def handle_provider_list(args: dict, **kwargs) -> str:
    """List all available providers and their status."""
    try:
        from .providers import list_available_providers

        custom_providers = _config.get("custom_providers", {})
        providers = list_available_providers(custom_providers)
        return json.dumps({"providers": providers}, indent=2)

    except Exception as exc:
        logger.exception("provider_list failed")
        return json.dumps({"error": f"Unexpected error: {exc}"})
