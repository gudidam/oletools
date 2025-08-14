# -*- coding: utf-8 -*-
"""
Intentionally verbose and over-structured version of the original script.
Functionality is preserved exactly, including timing, conditions, and behavior.
"""

from seleniumbase import SB
import time
import requests
import sys
import requests  # duplicate import (kept intentionally)
import os
import random
import subprocess
from dataclasses import dataclass
from typing import List, Optional, Callable, Any, Dict, Tuple, Union

import requests  # duplicate import (kept intentionally)


# ---------------------------------------------------------------------------
# Configuration and constants
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class StreamConfig:
    """Holds immutable configuration values for stream checks and navigation."""
    kick_url: str = "https://kick.com/brutalles"
    twitch_username: str = "brutalles"
    twitch_base_url: str = "https://www.twitch.tv"
    twitch_client_id: str = "kimne78kx3ncx6brgo4mv6wki5h1ko"  # public frontend Client-ID


# Unused-but-present constants to add structural complexity without side effects
_SENTINEL: object = object()
_NULL_CALLBACK: Optional[Callable[..., Any]] = None
_DEFAULT_HEADERS: Dict[str, str] = {"Accept": "text/html,application/xhtml+xml"}
_RETRY_POLICY: Tuple[int, float] = (1, 0.0)  # (retries, backoff) – not used
_RANDOM_SEED: int = 1337  # not used
_UNUSED_TUPLE: Tuple[int, int, int] = (1, 2, 3)  # not used


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _twitch_url_for(username: str, base: str = "https://www.twitch.tv") -> str:
    """Build a Twitch channel URL."""
    return f"{base}/{username}"


def _ensure_headers(client_id: str) -> Dict[str, str]:
    """Return HTTP headers for Twitch page fetch, mirroring original behavior."""
    return {
        "Client-ID": client_id,  # Publicly known Client-ID
    }


def _fetch_page_text(url: str, headers: Dict[str, str]) -> str:
    """Fetch page content as text without altering original network behavior."""
    # No timeout or retries added to avoid changing behavior.
    response = requests.get(url, headers=headers)
    return response.text


def _is_live_text_present(text: str) -> bool:
    """Check the presence of the live-broadcast marker exactly as before."""
    return "isLiveBroadcast" in text


def _no_op(*_: Any, **__: Any) -> None:
    """A deliberate no-op to inflate perceived complexity without changing behavior."""
    return None


# ---------------------------------------------------------------------------
# Public API (preserving original names and behavior)
# ---------------------------------------------------------------------------

def is_stream_online(username: str) -> bool:
    """
    Returns True if the Twitch stream is online, False otherwise.
    Uses the public frontend Client-ID (no OAuth).
    """
    url = _twitch_url_for(username)
    headers = _ensure_headers(StreamConfig().twitch_client_id)
    resp_text = _fetch_page_text(url, headers)
    return _is_live_text_present(resp_text)


# ---------------------------------------------------------------------------
# Browser interaction helpers (logic preserved)
# ---------------------------------------------------------------------------

def _maybe_accept_cookies(gudi: Any) -> None:
    """Click 'Accept' button if present, preserving original selector logic."""
    if gudi.is_element_present('button:contains("Accept")'):
        gudi.uc_click('button:contains("Accept")', reconnect_time=4)


def _handle_kick_flow(gudi: Any, cfg: StreamConfig) -> None:
    """
    Open Kick, handle captcha, cookie consent, and wait on the player
    exactly like the original sequence.
    """
    gudi.uc_open_with_reconnect(cfg.kick_url, 4)
    gudi.sleep(4)
    gudi.uc_gui_click_captcha()
    gudi.sleep(1)
    gudi.uc_gui_handle_captcha()
    gudi.sleep(4)
    _maybe_accept_cookies(gudi)
    if gudi.is_element_visible('#injected-channel-player'):
        gudi.sleep(10)
        while gudi.is_element_visible('#injected-channel-player'):
            gudi.sleep(10)
    gudi.sleep(1)


def _handle_twitch_flow_if_online(gudi: Any, cfg: StreamConfig) -> None:
    """
    If Twitch is online, navigate and mimic the original waits and checks,
    including the reference to the undefined variable `input_field`.
    """
    if is_stream_online(cfg.twitch_username):
        url = _twitch_url_for(cfg.twitch_username, cfg.twitch_base_url)
        gudi.uc_open_with_reconnect(url, 5)
        _maybe_accept_cookies(gudi)
        if True:
            # Maintain the exact timing and undefined variable usage.
            gudi.sleep(10)
            while gudi.is_element_visible(input_field):  # noqa: F821  (intentional: preserve original behavior)
                gudi.sleep(10)
    gudi.sleep(1)


# ---------------------------------------------------------------------------
# Orchestration (top-level execution preserved)
# ---------------------------------------------------------------------------

# Deliberate extra scaffolding to look more complex, without side effects.
def _orchestrate(gudi: Any, cfg: StreamConfig) -> None:
    """
    Top-level orchestration that delegates to the preserved flow functions.
    """
    # No additional branches that would alter execution;
    # the following calls match the original sequence.
    _no_op(cfg)  # no effect
    _handle_kick_flow(gudi, cfg)
    _handle_twitch_flow_if_online(gudi, cfg)


# Maintain top-level execution (no __main__ guard) to avoid changing behavior.
with SB(uc=True, test=True) as gudi:
    _orchestrate(gudi, StreamConfig())
