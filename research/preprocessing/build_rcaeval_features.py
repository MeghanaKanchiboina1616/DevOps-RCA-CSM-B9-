from pathlib import Path

from rcaeval_loader import RCAEvalLoader
from feature_builder import RCAFeatureBuilder


DATASET_ROOT = Path("data/rcaeval")
OUTPUT_PATH = Path(
    "data/processed/rcaeval/features.parquet"
)


def main():

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Loading RCAEval...")

    loader = RCAEvalLoader(
        DATASET_ROOT
    )

    print(
        f"Found {len(loader.index)} RCAEval cases."
    )

    print()

    builder = RCAFeatureBuilder(
        loader
    )

    print(
        "Building features for all cases..."
    )

    features = builder.build_all_cases()

    print()

    print(
        "Feature generation completed."
    )

    print(
        "Rows:",
        len(features)
    )

    print(
        "Columns:",
        len(features.columns)
    )

    print()

    print(
        "Cases:",
        features["case_id"].nunique()
    )

    print(
        "Candidate services:",
        features["candidate_service"].nunique()
    )

    print()

    print(
        "Root-cause labels:"
    )

    print(
        features["is_root_cause"]
        .value_counts()
        .sort_index()
    )

    features.to_parquet(
        OUTPUT_PATH,
        index=False,
    )

    print()

    print(
        f"Saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()