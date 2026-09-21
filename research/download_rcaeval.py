from huggingface_hub import snapshot_download

print("Starting complete RCAEval download...")
print("This may take some time because the dataset is large.")

snapshot_download(
    repo_id="phamquiluan/RCAEval",
    repo_type="dataset",
    local_dir="data/rcaeval",
)

print("\nRCAEval download completed successfully.")