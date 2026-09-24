from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


@dataclass
class RCAEvalCase:
    """
    Structured representation of one RCAEval failure case.
    """

    case_id: str
    dataset: str
    suite: str
    system: str
    system_name: str

    root_cause_service: str
    fault: str
    fault_description: str

    repetition: int
    inject_time: int

    normal_timesteps: int
    faulty_timesteps: int

    has_logs: bool
    has_traces: bool

    metrics: pd.DataFrame

    @property
    def normal_metrics(self) -> pd.DataFrame:
        """Telemetry before fault injection."""
        return self.metrics[self.metrics["time"] < self.inject_time].copy()

    @property
    def faulty_metrics(self) -> pd.DataFrame:
        """Telemetry from fault injection onward."""
        return self.metrics[self.metrics["time"] >= self.inject_time].copy()

    @property
    def metric_columns(self) -> list[str]:
        """Return all telemetry columns except the timestamp."""
        return [
            column
            for column in self.metrics.columns
            if column != "time"
        ]


class RCAEvalLoader:
    """
    Loads RCAEval metadata and individual failure cases.

    Expected dataset structure:

        data/rcaeval/
        ├── cases.parquet
        ├── re1ob_adservice_cpu_1/
        │   ├── metrics.parquet
        │   └── inject_time.txt
        └── ...

    The loader does not modify the original dataset.
    """

    def __init__(self, dataset_root: str | Path):
        self.dataset_root = Path(dataset_root)

        if not self.dataset_root.exists():
            raise FileNotFoundError(
                f"RCAEval directory not found: {self.dataset_root}"
            )

        self.index_path = self.dataset_root / "cases.parquet"

        if not self.index_path.exists():
            raise FileNotFoundError(
                f"RCAEval case index not found: {self.index_path}"
            )

        self.index = pd.read_parquet(self.index_path)

    def list_cases(
        self,
        dataset: Optional[str] = None,
        suite: Optional[str] = None,
        system_name: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Return cases matching optional filters.
        """

        df = self.index.copy()

        if dataset is not None:
            df = df[df["dataset"] == dataset]

        if suite is not None:
            df = df[df["suite"] == suite]

        if system_name is not None:
            df = df[df["system_name"] == system_name]

        return df.reset_index(drop=True)

    def get_case_metadata(self, case_id: str) -> pd.Series:
        """Return metadata for one case."""

        matches = self.index[self.index["case"] == case_id]

        if matches.empty:
            raise ValueError(
                f"RCAEval case not found: {case_id}"
            )

        return matches.iloc[0]

    def load_case(self, case_id: str) -> RCAEvalCase:
        """
        Load metadata + metric telemetry for one RCAEval case.
        """

        metadata = self.get_case_metadata(case_id)

        case_dir = self.dataset_root / case_id

        if not case_dir.exists():
            raise FileNotFoundError(
                f"Case directory not found: {case_dir}"
            )

        metrics_path = case_dir / "metrics.parquet"
        inject_time_path = case_dir / "inject_time.txt"

        if not metrics_path.exists():
            raise FileNotFoundError(
                f"Metrics file not found: {metrics_path}"
            )

        if not inject_time_path.exists():
            raise FileNotFoundError(
                f"Injection timestamp not found: {inject_time_path}"
            )

        metrics = pd.read_parquet(metrics_path)

        inject_time = int(
            inject_time_path.read_text(encoding="utf-8").strip()
        )

        if "time" not in metrics.columns:
            raise ValueError(
                f"Case {case_id} does not contain required 'time' column."
            )

        metrics = metrics.sort_values("time").reset_index(drop=True)

        normal_metrics = metrics[
            metrics["time"] < inject_time
        ]

        faulty_metrics = metrics[
            metrics["time"] >= inject_time
        ]

        return RCAEvalCase(
            case_id=str(metadata["case"]),
            dataset=str(metadata["dataset"]),
            suite=str(metadata["suite"]),
            system=str(metadata["system"]),
            system_name=str(metadata["system_name"]),
            root_cause_service=str(
                metadata["root_cause_service"]
            ),
            fault=str(metadata["fault"]),
            fault_description=str(
                metadata["fault_description"]
            ),
            repetition=int(metadata["repetition"]),
            inject_time=inject_time,
            normal_timesteps=len(normal_metrics),
            faulty_timesteps=len(faulty_metrics),
            has_logs=bool(metadata["has_logs"]),
            has_traces=bool(metadata["has_traces"]),
            metrics=metrics,
        )