"""Shared prompt constants and formatting helpers."""

CONTINUE_REMINDER = "Keep this in mind as you continue with the next task."

FORMAT_ERROR = (
    r"Note: your previous response did not include a \bbox{X} answer "
    r"(e.g. \bbox{A} for a single option, or \bbox{A,B} for multiple options). "
    + CONTINUE_REMINDER
)


def missed_option(opt: str, explanation: str) -> str:
    return f"You missed option {opt}: {explanation}"


def wrong_option(opt: str, explanation: str) -> str:
    return f"You incorrectly selected option {opt}: {explanation}"


FILE_CHECK_INCORRECT_SUFFIX = CONTINUE_REMINDER

# ── multi_choice: answer format instruction ───────────────────────────
MULTI_CHOICE_INSTRUCTION = (
    r"\nSelect all correct statements, and answer with \bbox{X,Y,...} format directly."
)

# ── update notification ───────────────────────────────────────────────
UPDATE_NOTES = r"The workspace and messages in other channels are updated.\n"

_FEEDBACK_MARKER = "[Previous Feedback]"


def with_feedback(feedback_text: str, question_text: str) -> str:
    return f"{_FEEDBACK_MARKER} {feedback_text}\n\n{question_text}"


def standalone_feedback(feedback_text: str) -> str:
    return f"{_FEEDBACK_MARKER} {feedback_text}"
