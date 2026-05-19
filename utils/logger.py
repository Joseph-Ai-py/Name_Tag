"""
Enhanced logging system for NameTag with detailed variable tracking.
Provides structured logging, variable tracking, and Docker-friendly output.
"""
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# Create logs directory if it doesn't exist
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log file paths
LOG_FILE = LOG_DIR / "nametag.log"
VARIABLE_LOG_FILE = LOG_DIR / "variables.jsonl"


class StructuredFormatter(logging.Formatter):
    """
    Structured formatter for logs with variable tracking.
    """

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now().isoformat()
        level = record.levelname

        # Build base log message
        log_data = {
            "timestamp": timestamp,
            "level": level,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields if present
        if hasattr(record, "variables"):
            log_data["variables"] = record.variables
        if hasattr(record, "step"):
            log_data["step"] = record.step
        if hasattr(record, "session_id"):
            log_data["session_id"] = record.session_id

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


class PlainFormatter(logging.Formatter):
    """Human-readable formatter for console output."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level = record.levelname
        logger = record.name

        # Build message with variables if present
        msg = f"[{timestamp}] {level:8} {logger:30}"

        if hasattr(record, "session_id"):
            msg += f" [SID:{record.session_id}]"

        msg += f" {record.getMessage()}"

        if hasattr(record, "variables"):
            msg += f" | Variables: {json.dumps(record.variables, ensure_ascii=False)}"

        if record.exc_info:
            msg += f"\n{self.formatException(record.exc_info)}"

        return msg


def setup_logger(name: str, session_id: Optional[str] = None) -> logging.Logger:
    """
    Setup a logger with both file and console handlers.

    Args:
        name: Logger name
        session_id: Optional session ID for tracking

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers
    logger.handlers.clear()

    # File handler (JSON format for parsing)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(StructuredFormatter())
    logger.addHandler(file_handler)

    # Console handler (readable format)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(PlainFormatter())
    logger.addHandler(console_handler)

    logger.session_id = session_id
    return logger


class VariableTracker:
    """
    Track and log variables during generation process.
    """

    def __init__(self, session_id: str, logger: logging.Logger):
        self.session_id = session_id
        self.logger = logger
        self.variables: dict[str, Any] = {}
        self.steps: list[dict[str, Any]] = []

    def set_variable(
        self,
        name: str,
        value: Any,
        source: str = "user",
        description: str = "",
    ) -> None:
        """
        Record a variable value.

        Args:
            name: Variable name (e.g., BRAND_NAME, TARGET_MOOD)
            value: Variable value
            source: Source of value (user, ai_recommended, auto_inferred, ai_response)
            description: Optional description
        """
        self.variables[name] = {
            "value": value,
            "source": source,
            "description": description,
            "timestamp": datetime.now().isoformat(),
        }

        # Log to JSON file
        self._log_variable(name, value, source)

        # Log via logger
        self.logger.debug(
            f"Variable set: {name}",
            extra={
                "variables": {name: value},
                "session_id": self.session_id,
            },
        )

    def set_ai_response(self, response_data: dict[str, Any]) -> None:
        """
        Record AI response with all extracted variables.

        Args:
            response_data: Dict containing AI response and extracted variables
        """
        step_record = {
            "timestamp": datetime.now().isoformat(),
            "step": f"ai_response_{len(self.steps)}",
            "response_raw": response_data.get("raw_response", ""),
            "extracted_variables": response_data.get("variables", {}),
            "metadata": response_data.get("metadata", {}),
        }

        self.steps.append(step_record)

        # Update variables from AI response
        for var_name, var_value in response_data.get("variables", {}).items():
            self.set_variable(var_name, var_value, source="ai_response")

        # Log AI response
        self.logger.info(
            f"AI Response processed: {len(response_data.get('variables', {}))} variables extracted",
            extra={
                "variables": response_data.get("variables", {}),
                "session_id": self.session_id,
                "step": "ai_response",
            },
        )

    def _log_variable(self, name: str, value: Any, source: str) -> None:
        """Write variable to JSONL file."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "variable_name": name,
            "variable_value": str(value),
            "source": source,
        }
        with open(VARIABLE_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def get_all_variables(self) -> dict[str, Any]:
        """Get all tracked variables."""
        return {
            name: data["value"] for name, data in self.variables.items()
        }

    def get_variable_sources(self) -> dict[str, str]:
        """Get source information for each variable."""
        return {
            name: data["source"] for name, data in self.variables.items()
        }

    def log_step(self, step_name: str, details: dict[str, Any]) -> None:
        """Log a processing step."""
        step_record = {
            "timestamp": datetime.now().isoformat(),
            "step": step_name,
            "details": details,
        }
        self.steps.append(step_record)

        self.logger.info(
            f"Step: {step_name}",
            extra={
                "step": step_name,
                "session_id": self.session_id,
                "variables": details,
            },
        )

    def export_session_log(self) -> dict[str, Any]:
        """Export complete session log."""
        return {
            "session_id": self.session_id,
            "start_time": self.steps[0]["timestamp"] if self.steps else None,
            "end_time": datetime.now().isoformat(),
            "variables": self.variables,
            "steps": self.steps,
        }


# Module-level convenience functions
_loggers: dict[str, logging.Logger] = {}
_trackers: dict[str, VariableTracker] = {}


def get_logger(name: str, session_id: Optional[str] = None) -> logging.Logger:
    """Get or create a logger."""
    key = f"{name}_{session_id}"
    if key not in _loggers:
        _loggers[key] = setup_logger(name, session_id)
    return _loggers[key]


def get_tracker(session_id: str) -> VariableTracker:
    """Get or create a variable tracker."""
    if session_id not in _trackers:
        logger = get_logger("NameTag.Tracker", session_id)
        _trackers[session_id] = VariableTracker(session_id, logger)
    return _trackers[session_id]
