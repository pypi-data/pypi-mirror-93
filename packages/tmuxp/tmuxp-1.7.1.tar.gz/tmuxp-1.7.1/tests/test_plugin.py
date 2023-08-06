# -*- coding: utf-8 -*-
"""Test for tmuxp plugin api."""
from __future__ import absolute_import

import pytest

from tmuxp.exc import TmuxpPluginException

from .fixtures.pluginsystem.partials.all_pass import AllVersionPassPlugin
from .fixtures.pluginsystem.partials.libtmux_version_fail import (
    LibtmuxVersionFailIncompatiblePlugin,
    LibtmuxVersionFailMaxPlugin,
    LibtmuxVersionFailMinPlugin,
)
from .fixtures.pluginsystem.partials.tmux_version_fail import (
    TmuxVersionFailIncompatiblePlugin,
    TmuxVersionFailMaxPlugin,
    TmuxVersionFailMinPlugin,
)
from .fixtures.pluginsystem.partials.tmuxp_version_fail import (
    TmuxpVersionFailIncompatiblePlugin,
    TmuxpVersionFailMaxPlugin,
    TmuxpVersionFailMinPlugin,
)


def test_all_pass():
    AllVersionPassPlugin()


def test_tmux_version_fail_min():
    with pytest.raises(TmuxpPluginException, match=r'Incompatible.*') as exc_info:
        TmuxVersionFailMinPlugin()
    assert 'tmux-min-version-fail' in str(exc_info.value)


def test_tmux_version_fail_max():
    with pytest.raises(TmuxpPluginException, match=r'Incompatible.*') as exc_info:
        TmuxVersionFailMaxPlugin()
    assert 'tmux-max-version-fail' in str(exc_info.value)


def test_tmux_version_fail_incompatible():
    with pytest.raises(TmuxpPluginException, match=r'Incompatible.*') as exc_info:
        TmuxVersionFailIncompatiblePlugin()
    assert 'tmux-incompatible-version-fail' in str(exc_info.value)


def test_tmuxp_version_fail_min():
    with pytest.raises(TmuxpPluginException, match=r'Incompatible.*') as exc_info:
        TmuxpVersionFailMinPlugin()
    assert 'tmuxp-min-version-fail' in str(exc_info.value)


def test_tmuxp_version_fail_max():
    with pytest.raises(TmuxpPluginException, match=r'Incompatible.*') as exc_info:
        TmuxpVersionFailMaxPlugin()
    assert 'tmuxp-max-version-fail' in str(exc_info.value)


def test_tmuxp_version_fail_incompatible():
    with pytest.raises(TmuxpPluginException, match=r'Incompatible.*') as exc_info:
        TmuxpVersionFailIncompatiblePlugin()
    assert 'tmuxp-incompatible-version-fail' in str(exc_info.value)


def test_libtmux_version_fail_min():
    with pytest.raises(TmuxpPluginException, match=r'Incompatible.*') as exc_info:
        LibtmuxVersionFailMinPlugin()
    assert 'libtmux-min-version-fail' in str(exc_info.value)


def test_libtmux_version_fail_max():
    with pytest.raises(TmuxpPluginException, match=r'Incompatible.*') as exc_info:
        LibtmuxVersionFailMaxPlugin()
    assert 'libtmux-max-version-fail' in str(exc_info.value)


def test_libtmux_version_fail_incompatible():
    with pytest.raises(TmuxpPluginException, match=r'Incompatible.*') as exc_info:
        LibtmuxVersionFailIncompatiblePlugin()
    assert 'libtmux-incompatible-version-fail' in str(exc_info.value)
