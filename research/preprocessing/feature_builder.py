from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

from rcaeval_loader import RCAEvalLoader


@dataclass
class MetricFeatures:
    """
    Statistical and temporal features for one telemetry metric.
    """

    mean_change: float
    relative_change: float

    max_change: float
    std_change: float

    early_relative_change: float
    late_relative_change: float

    deviation_fraction: float

    available: int


class RCAFeatureBuilder:
    """
    Converts RCAEval telemetry into service-level RCA features.

    The builder compares the normal period before fault injection
    against the faulty period after injection.
    """

    METRIC_TYPES = [
        "cpu",
        "mem",
        "load",
        "latency",
        "error",
    ]

    def __init__(self, loader: RCAEvalLoader):
        self.loader = loader

    @staticmethod
    def _safe_relative_change(
        normal_mean: float,
        fault_mean: float,
    ) -> float:
        """
        Calculate relative change safely.

        Returns 0 when the metric has no meaningful normal baseline.
        """

        if not np.isfinite(normal_mean):
            return 0.0

        if not np.isfinite(fault_mean):
            return 0.0

        denominator = abs(normal_mean)

        if denominator < 1e-8:
            return 0.0

        return (fault_mean - normal_mean) / denominator

    @staticmethod
    def _empty_features() -> MetricFeatures:
        """
        Representation for a metric that does not exist.
        """

        return MetricFeatures(
            mean_change=0.0,
            relative_change=0.0,
            max_change=0.0,
            std_change=0.0,
            early_relative_change=0.0,
            late_relative_change=0.0,
            deviation_fraction=0.0,
            available=0,
        )

    @staticmethod
    def _metric_statistics(
        normal: pd.Series,
        faulty: pd.Series,
    ) -> MetricFeatures:
        """
        Calculate statistical and temporal features for one metric.
        """

        if normal.empty or faulty.empty:
            return RCAFeatureBuilder._empty_features()

        normal = pd.to_numeric(normal, errors="coerce").dropna()
        faulty = pd.to_numeric(faulty, errors="coerce").dropna()

        if normal.empty or faulty.empty:
            return RCAFeatureBuilder._empty_features()

        normal_mean = float(normal.mean())
        faulty_mean = float(faulty.mean())

        normal_max = float(normal.max())
        faulty_max = float(faulty.max())

        normal_std = float(normal.std())
        faulty_std = float(faulty.std())

        mean_change = faulty_mean - normal_mean

        relative_change = (
            RCAFeatureBuilder._safe_relative_change(
                normal_mean,
                faulty_mean,
            )
        )

        max_change = faulty_max - normal_max

        std_change = faulty_std - normal_std

        # ---------------------------------------------------------
        # Early fault window
        # ---------------------------------------------------------

        early_count = max(1, int(len(faulty) * 0.25))

        early_fault = faulty.iloc[:early_count]

        early_mean = float(early_fault.mean())

        early_relative_change = (
            RCAFeatureBuilder._safe_relative_change(
                normal_mean,
                early_mean,
            )
        )

        # ---------------------------------------------------------
        # Late fault window
        # ---------------------------------------------------------

        late_count = max(1, int(len(faulty) * 0.25))

        late_fault = faulty.iloc[-late_count:]

        late_mean = float(late_fault.mean())

        late_relative_change = (
            RCAFeatureBuilder._safe_relative_change(
                normal_mean,
                late_mean,
            )
        )

        # ---------------------------------------------------------
        # Deviation fraction
        # ---------------------------------------------------------

        baseline_std = max(normal_std, 1e-8)

        deviation_threshold = 2.0 * baseline_std

        deviations = np.abs(
            faulty - normal_mean
        ) > deviation_threshold

        deviation_fraction = float(
            deviations.mean()
        )

        return MetricFeatures(
            mean_change=mean_change,
            relative_change=relative_change,
            max_change=max_change,
            std_change=std_change,
            early_relative_change=early_relative_change,
            late_relative_change=late_relative_change,
            deviation_fraction=deviation_fraction,
            available=1,
        )

    @staticmethod
    def _get_metric(
        df: pd.DataFrame,
        metric_name: str,
    ) -> pd.Series:
        """
        Return a metric if available.
        """

        if metric_name not in df.columns:
            return pd.Series(dtype=float)

        return df[metric_name]

    @staticmethod
    def discover_services(
        metrics: pd.DataFrame,
    ) -> List[str]:
        """
        Discover service names from telemetry columns.
        """

        services = set()

        for column in metrics.columns:

            if column == "time":
                continue

            for suffix in RCAFeatureBuilder.METRIC_TYPES:

                metric_suffix = f"_{suffix}"

                if column.endswith(metric_suffix):

                    service = column[
                        : -len(metric_suffix)
                    ]

                    if service:
                        services.add(service)

                    break

        return sorted(services)

    def _build_metric_features(
        self,
        normal: pd.DataFrame,
        faulty: pd.DataFrame,
        metric_name: str,
    ) -> MetricFeatures:

        normal_metric = self._get_metric(
            normal,
            metric_name,
        )

        faulty_metric = self._get_metric(
            faulty,
            metric_name,
        )

        return self._metric_statistics(
            normal_metric,
            faulty_metric,
        )

    def _build_service_features(
        self,
        service: str,
        normal: pd.DataFrame,
        faulty: pd.DataFrame,
    ) -> Dict[str, float]:

        features: Dict[str, float] = {}

        for metric_type in self.METRIC_TYPES:

            metric_name = f"{service}_{metric_type}"

            metric_features = self._build_metric_features(
                normal,
                faulty,
                metric_name,
            )

            prefix = metric_type

            features[
                f"{prefix}_mean_change"
            ] = metric_features.mean_change

            features[
                f"{prefix}_relative_change"
            ] = metric_features.relative_change

            features[
                f"{prefix}_max_change"
            ] = metric_features.max_change

            features[
                f"{prefix}_std_change"
            ] = metric_features.std_change

            features[
                f"{prefix}_early_relative_change"
            ] = metric_features.early_relative_change

            features[
                f"{prefix}_late_relative_change"
            ] = metric_features.late_relative_change

            features[
                f"{prefix}_deviation_fraction"
            ] = metric_features.deviation_fraction

            features[
                f"{prefix}_available"
            ] = metric_features.available

        return features

    def build_case(
        self,
        case_id: str,
    ) -> pd.DataFrame:
        """
        Build service-level RCA features for one case.

        Returns one row per candidate service.
        """

        case = self.loader.load_case(case_id)

        normal = case.normal_metrics
        faulty = case.faulty_metrics

        services = self.discover_services(
            case.metrics
        )

        rows = []

        for service in services:

            row = {
                "case_id": case.case_id,
                "dataset": case.dataset,
                "suite": case.suite,
                "system": case.system_name,
                "fault": case.fault,
                "candidate_service": service,
                "root_cause_service": case.root_cause_service,
            }

            service_features = (
                self._build_service_features(
                    service,
                    normal,
                    faulty,
                )
            )

            row.update(service_features)

            row["is_root_cause"] = int(
                service == case.root_cause_service
            )

            rows.append(row)

        return pd.DataFrame(rows)

    def build_all_cases(
        self,
        case_ids: List[str] | None = None,
    ) -> pd.DataFrame:
        """
        Build features for multiple RCAEval cases.
        """

        if case_ids is None:
            case_ids = self.loader.index[
                "case"
            ].tolist()

        all_features = []

        total = len(case_ids)

        for index, case_id in enumerate(
            case_ids,
            start=1,
        ):

            print(
                f"[{index}/{total}] Processing {case_id}"
            )

            case_features = self.build_case(
                case_id
            )

            all_features.append(
                case_features
            )

        if not all_features:
            return pd.DataFrame()

        return pd.concat(
            all_features,
            ignore_index=True,
        )