from pathlib import Path

from rcaeval_loader import RCAEvalLoader
from feature_builder import RCAFeatureBuilder


DATASET_ROOT = Path("data/rcaeval")


def main():

    loader = RCAEvalLoader(DATASET_ROOT)

    builder = RCAFeatureBuilder(loader)

    case_id = "re1ob_adservice_cpu_1"

    features = builder.build_case(case_id)

    print("===== FEATURE BUILDER =====")
    print("Case:", case_id)
    print("Candidate services:", len(features))
    print()

    print("Columns:")
    print(features.columns.tolist())
    print()

    print("===== SERVICE FEATURES =====")
    print(
        features[
            [
                "candidate_service",
                "cpu_relative_change",
                "mem_relative_change",
                "load_relative_change",
                "latency_relative_change",
                "error_relative_change",
                "is_root_cause",
            ]
        ].to_string(index=False)
    )

    print()

    print("===== ROOT CAUSE =====")

    root = features[
        features["is_root_cause"] == 1
    ]

    print(root.to_string(index=False))


if __name__ == "__main__":
    main()