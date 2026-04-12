"""
continuous_intelligence_abdelhafidh.py - Custom project script.

Author: Abdelhafidh Mahouel
Date: 2026-04

System Metrics Data

- Data represents recent observations from a monitored system.
- Each row represents one observation of system activity.

CSV columns:
- requests: number of requests handled
- errors: number of failed requests
- total_latency_ms: total response time in milliseconds

Purpose

- Read system metrics from a CSV file.
- Apply continuous intelligence techniques:
  - signal design
  - anomaly detection
  - simple drift-style reasoning
- Summarize the system's current state.
- Save the resulting system assessment as a CSV artifact.
- Log the pipeline process for transparency and debugging.

Paths (relative to repo root)

    INPUT FILE: data/system_metrics_abdelhafidh.csv
    OUTPUT FILE: artifacts/system_assessment_abdelhafidh.csv

Terminal command to run this file from the root project folder

    uv run python -m cintel.continuous_intelligence_abdelhafidh
"""

# === DECLARE IMPORTS ===

import logging
from pathlib import Path
from typing import Final

import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P6", level="DEBUG")

# === DEFINE GLOBAL PATHS ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

DATA_FILE: Final[Path] = DATA_DIR / "system_metrics_abdelhafidh.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "system_assessment_abdelhafidh.csv"

# === DEFINE THRESHOLDS ===

MAX_ERROR_RATE: Final[float] = 0.04
MAX_AVG_LATENCY: Final[float] = 35.0
MIN_REQUESTS: Final[int] = 1


# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Run the custom continuous intelligence pipeline."""
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    # Ensure artifacts directory exists
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # ----------------------------------------------------
    # STEP 1: READ SYSTEM METRICS
    # ----------------------------------------------------
    df = pl.read_csv(DATA_FILE)
    LOG.info(f"STEP 1. Loaded {df.height} system records")

    # ----------------------------------------------------
    # STEP 2: VALIDATE INPUT DATA
    # ----------------------------------------------------
    LOG.info("STEP 2. Validating input data...")

    df = df.filter(pl.col("requests") >= MIN_REQUESTS)

    LOG.info(f"STEP 2. Records after validation: {df.height}")

    # ----------------------------------------------------
    # STEP 3: DESIGN SIGNALS
    # ----------------------------------------------------
    LOG.info("STEP 3. Designing signals from raw metrics...")

    df = df.with_columns(
        [
            (pl.col("errors") / pl.col("requests")).alias("error_rate"),
            (pl.col("total_latency_ms") / pl.col("requests")).alias("avg_latency_ms"),
            ((pl.col("requests") - pl.col("errors")) / pl.col("requests")).alias(
                "success_rate"
            ),
            (pl.col("total_latency_ms") / (pl.col("errors") + 1)).alias(
                "latency_per_error"
            ),
        ]
    )

    # ----------------------------------------------------
    # STEP 4: DETECT ANOMALIES
    # ----------------------------------------------------
    LOG.info("STEP 4. Checking for anomalies in system signals...")

    df = df.with_columns(
        pl.when(
            (pl.col("error_rate") > MAX_ERROR_RATE)
            & (pl.col("avg_latency_ms") > MAX_AVG_LATENCY)
        )
        .then(pl.lit("high error rate and high latency"))
        .when(pl.col("error_rate") > MAX_ERROR_RATE)
        .then(pl.lit("high error rate"))
        .when(pl.col("avg_latency_ms") > MAX_AVG_LATENCY)
        .then(pl.lit("high latency"))
        .otherwise(pl.lit("normal"))
        .alias("anomaly_reason")
    )

    anomalies_df = df.filter(pl.col("anomaly_reason") != "normal")

    LOG.info(
        f"STEP 4. Using thresholds: MAX_ERROR_RATE={MAX_ERROR_RATE}, "
        f"MAX_AVG_LATENCY={MAX_AVG_LATENCY}"
    )
    LOG.info(f"STEP 4. Anomalies detected: {anomalies_df.height}")

    # ----------------------------------------------------
    # STEP 5: CHECK SIMPLE DRIFT
    # ----------------------------------------------------
    LOG.info("STEP 5. Checking for simple drift between first and second half...")

    midpoint = df.height // 2

    first_half = df.slice(0, midpoint)
    second_half = df.slice(midpoint, df.height - midpoint)

    first_half_error_rate = (
        first_half.select(pl.col("error_rate").mean()).item()
        if first_half.height > 0
        else 0.0
    )
    second_half_error_rate = (
        second_half.select(pl.col("error_rate").mean()).item()
        if second_half.height > 0
        else 0.0
    )

    first_half_latency = (
        first_half.select(pl.col("avg_latency_ms").mean()).item()
        if first_half.height > 0
        else 0.0
    )
    second_half_latency = (
        second_half.select(pl.col("avg_latency_ms").mean()).item()
        if second_half.height > 0
        else 0.0
    )

    if (
        second_half_error_rate > first_half_error_rate
        and second_half_latency > first_half_latency
    ):
        drift_status = "worsening"
    elif (
        second_half_error_rate < first_half_error_rate
        and second_half_latency < first_half_latency
    ):
        drift_status = "improving"
    else:
        drift_status = "mixed"

    LOG.info(f"STEP 5. Drift status: {drift_status}")

    # ----------------------------------------------------
    # STEP 6: SUMMARIZE CURRENT SYSTEM STATE
    # ----------------------------------------------------
    LOG.info("STEP 6. Summarizing system state from monitored signals...")

    summary_df = df.select(
        [
            pl.col("requests").mean().alias("avg_requests"),
            pl.col("errors").mean().alias("avg_errors"),
            pl.col("error_rate").mean().alias("avg_error_rate"),
            pl.col("avg_latency_ms").mean().alias("avg_latency_ms"),
            pl.col("success_rate").mean().alias("avg_success_rate"),
            pl.col("latency_per_error").mean().alias("avg_latency_per_error"),
        ]
    )

    anomaly_count = anomalies_df.height
    total_records = df.height
    anomaly_percent = (anomaly_count / total_records) if total_records > 0 else 0.0

    summary_df = summary_df.with_columns(
        [
            pl.lit(anomaly_count).alias("anomaly_count"),
            pl.lit(round(anomaly_percent, 4)).alias("anomaly_percent"),
            pl.lit(round(first_half_error_rate, 4)).alias("first_half_error_rate"),
            pl.lit(round(second_half_error_rate, 4)).alias("second_half_error_rate"),
            pl.lit(round(first_half_latency, 4)).alias("first_half_avg_latency_ms"),
            pl.lit(round(second_half_latency, 4)).alias("second_half_avg_latency_ms"),
            pl.lit(drift_status).alias("drift_status"),
        ]
    )

    summary_df = summary_df.with_columns(
        pl.when(
            (pl.col("avg_error_rate") > MAX_ERROR_RATE)
            | (pl.col("avg_latency_ms") > MAX_AVG_LATENCY)
            | (pl.col("anomaly_percent") > 0.30)
        )
        .then(pl.lit("DEGRADED"))
        .otherwise(pl.lit("STABLE"))
        .alias("system_state")
    )

    LOG.info("STEP 6. System assessment completed")

    # ----------------------------------------------------
    # STEP 7: SAVE OUTPUTS
    # ----------------------------------------------------
    summary_df.write_csv(OUTPUT_FILE)
    LOG.info(f"STEP 7. Wrote system assessment file: {OUTPUT_FILE}")

    anomaly_output_file = ARTIFACTS_DIR / "system_anomalies_abdelhafidh.csv"
    anomalies_df.write_csv(anomaly_output_file)
    LOG.info(f"STEP 7. Wrote anomalies file: {anomaly_output_file}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
