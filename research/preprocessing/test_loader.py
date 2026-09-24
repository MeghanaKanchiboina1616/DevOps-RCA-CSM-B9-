from pathlib import Path

from rcaeval_loader import RCAEvalLoader


DATASET_ROOT = Path("data/rcaeval")


def main():
    loader = RCAEvalLoader(DATASET_ROOT)

    print("RCAEval cases:", len(loader.index))
    print()

    case_id = "re1ob_adservice_cpu_1"

    case = loader.load_case(case_id)

    print("===== CASE =====")
    print("Case:", case.case_id)
    print("Dataset:", case.dataset)
    print("Suite:", case.suite)
    print("System:", case.system_name)
    print("Root cause service:", case.root_cause_service)
    print("Fault:", case.fault)
    print("Injection time:", case.inject_time)
    print()

    print("===== TELEMETRY =====")
    print("Total rows:", len(case.metrics))
    print("Normal rows:", len(case.normal_metrics))
    print("Faulty rows:", len(case.faulty_metrics))
    print("Metric count:", len(case.metric_columns))
    print()

    print("===== METRICS =====")
    print(case.metric_columns)

    print()
    print("===== NORMAL DATA =====")
    print(case.normal_metrics.head(3).to_string(index=False))

    print()
    print("===== FAULT DATA =====")
    print(case.faulty_metrics.head(3).to_string(index=False))


if __name__ == "__main__":
    main()