from pathlib import Path

from jarvis.commands import build_router


def test_time_command_returns_a_response(tmp_path: Path) -> None:
    result = build_router(tmp_path / "notes.md").dispatch("the time")
    assert result.response.startswith("It is ")


def test_note_command_persists_text(tmp_path: Path) -> None:
    notes = tmp_path / "notes.md"
    result = build_router(notes).dispatch("note buy more coffee")
    assert result.response == "Saved that note."
    assert "buy more coffee" in notes.read_text(encoding="utf-8")


def test_exit_command_stops_the_loop(tmp_path: Path) -> None:
    result = build_router(tmp_path / "notes.md").dispatch("goodbye")
    assert result.should_exit is True


def test_unknown_command_explains_next_step(tmp_path: Path) -> None:
    result = build_router(tmp_path / "notes.md").dispatch("play chess")
    assert "do not have a skill" in result.response
