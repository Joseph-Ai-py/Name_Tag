from __future__ import annotations

from typing import Any

import streamlit as st


def default_state() -> dict[str, Any]:
	return {
		"brand_data": None,
		"interview_data_o": "",
		"brand_info": None,
		"interview_data_a": "",
		"data_a": None,
		"interview_data_b": "",
		"data_b": None,
		"interview_data_c": "",
		"data_c": None,
		"interview_data_de": "",
		"data_de": None,
		"current_step": 0,
		"is_loading": False,
		"error": None,
		"interview_snapshots": {},
		"applied_selections": {},
	}


def initialize_session_state() -> None:
	for key, value in default_state().items():
		if key not in st.session_state:
			st.session_state[key] = value


def get_state(key: str) -> Any:
	initialize_session_state()
	return st.session_state.get(key)


def set_state(key: str, value: Any) -> None:
	initialize_session_state()
	st.session_state[key] = value


def reset_workflow_state() -> None:
	state = default_state()
	for key, value in state.items():
		st.session_state[key] = value


def save_interview_snapshot(section_key: str, snapshot: dict[str, Any]) -> None:
	initialize_session_state()
	snapshots = dict(st.session_state.get("interview_snapshots") or {})
	base = dict(snapshots.get(section_key) or {})
	base.update(snapshot)
	snapshots[section_key] = base
	st.session_state["interview_snapshots"] = snapshots


def load_interview_snapshot(section_key: str) -> dict[str, Any] | None:
	initialize_session_state()
	snapshots = st.session_state.get("interview_snapshots") or {}
	data = snapshots.get(section_key)
	if data is None:
		return None
	return dict(data)


def clear_interview_snapshot(section_key: str) -> None:
	initialize_session_state()
	snapshots = dict(st.session_state.get("interview_snapshots") or {})
	snapshots.pop(section_key, None)
	st.session_state["interview_snapshots"] = snapshots


def set_applied_selection(section: str, field: str, value: str) -> None:
	initialize_session_state()
	selections = dict(st.session_state.get("applied_selections") or {})
	section_map = dict(selections.get(section) or {})
	section_map[field] = value
	selections[section] = section_map
	st.session_state["applied_selections"] = selections


def get_applied_selection(section: str, field: str) -> str | None:
	initialize_session_state()
	selections = st.session_state.get("applied_selections") or {}
	section_map = selections.get(section) or {}
	return section_map.get(field)


def clear_applied_selections(section: str | None = None) -> None:
	initialize_session_state()
	if section is None:
		st.session_state["applied_selections"] = {}
		return

	selections = dict(st.session_state.get("applied_selections") or {})
	selections.pop(section, None)
	st.session_state["applied_selections"] = selections

