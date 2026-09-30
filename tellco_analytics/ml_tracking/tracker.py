import os
import json
import time
import datetime
import pickle
import pandas as pd

class ModelTracker:
    def __init__(self, log_dir: str = "artifacts/mlops_tracking"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.run_history_file = os.path.join(self.log_dir, "run_history.json")

    def start_run(self, run_name: str, source: str = "scripts/run_pipeline.py", code_version: str = "v1.0.0") -> dict:
        return {
            "run_id": f"run_{int(time.time())}",
            "run_name": run_name,
            "source": source,
            "code_version": code_version,
            "start_time": datetime.datetime.now().isoformat(),
            "status": "RUNNING"
        }

    def log_run(self, run_ctx: dict, parameters: dict, metrics: dict, model_object=None, artifact_paths: list = None) -> dict:
        run_ctx["end_time"] = datetime.datetime.now().isoformat()
        run_ctx["status"] = "COMPLETED"
        run_ctx["parameters"] = parameters
        run_ctx["metrics"] = metrics
        run_ctx["artifact_paths"] = artifact_paths or []

        # Save model artifact if provided
        if model_object is not None:
            model_file = os.path.join(self.log_dir, f"{run_ctx['run_id']}_model.pkl")
            with open(model_file, "wb") as f:
                pickle.dump(model_object, f)
            run_ctx["artifact_paths"].append(model_file)

        # Update run history
        history = []
        if os.path.exists(self.run_history_file):
            try:
                with open(self.run_history_file, "r") as f:
                    history = json.load(f)
            except Exception:
                history = []

        history.append(run_ctx)

        with open(self.run_history_file, "w") as f:
            json.dump(history, f, indent=4)

        # Also write summary CSV file for easy reporting
        df_history = pd.DataFrame(history)
        csv_file = os.path.join(self.log_dir, "tracking_summary.csv")
        df_history.to_csv(csv_file, index=False)

        return run_ctx

    def get_run_history(self) -> list:
        if os.path.exists(self.run_history_file):
            with open(self.run_history_file, "r") as f:
                return json.load(f)
        return []
