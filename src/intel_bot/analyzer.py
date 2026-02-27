"""Analysis orchestration — delegates to crewAI-based multi-agent crew.

Public API:
    analyze_all(settings, on_progress) -> AnalysisRun
"""

from intel_bot.crew import analyze_all

__all__ = ["analyze_all"]
