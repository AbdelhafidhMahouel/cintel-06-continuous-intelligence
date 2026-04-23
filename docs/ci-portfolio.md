# Continuous Intelligence Portfolio
**Abdelhafidh Mahouel**
2026-04
<p align="center">
  <img src="../images/ci-banner.png" width="900">
</p>

This page summarizes my work on continuous intelligence projects, highlighting key techniques, datasets, and insights gained throughout the course.

---

## 1. Professional Project

### Repository Link
[View Repository](https://github.com/AbdelhafidhMahouel/cintel-01-getting-started)

### Brief Overview of Project Tools and Choices
In this project, I set up and verified a Continuous Intelligence pipeline in my local environment. I copied the base pipeline and created my own version to explore how it works.

As a technical modification, I created a new file (`pipeline_abdelhafidh.py`) based on the original example. I added additional logging to improve observability, including logging the artifacts directory path and checking whether the `docs` and `artifacts` folders exist.

This modification helped me better understand how the pipeline executes and how to monitor its behavior through logs. It also confirmed that my environment was correctly configured and that the pipeline was running successfully.

---

## 2. Anomaly Detection

### Repository Link
[View Repository](https://github.com/AbdelhafidhMahouel/cintel-02-static-anomalies)

### Techniques
- Used static anomaly detection with predefined thresholds
- Modified threshold values to make detection more realistic
- Added both upper and lower bound validation for age and height
- Introduced a new column (`anomaly_reason`) to explain why each record was flagged

### Artifacts
[Artifacts Folder](https://github.com/AbdelhafidhMahouel/cintel-02-static-anomalies/tree/main/artifacts)

The output includes a new anomalies file where each flagged record contains a clear explanation of the reason it was detected.

### Insights
This project showed how sensitive anomaly detection is to threshold values. Small changes in thresholds significantly increased the number of detected anomalies.

Adding lower bounds improved detection completeness, while the `anomaly_reason` column made the results easier to understand and interpret. This helps analysts quickly identify the cause of anomalies instead of just seeing flagged values.

---

## 3. Signal Design

### Repository Link
[View Repository](https://github.com/AbdelhafidhMahouel/cintel-03-signal-design)

### Signals
- error_rate: errors / requests
- avg_latency_ms: total latency / requests
- throughput: number of requests per observation
- high_error_flag: binary signal (1 if error_rate > 5%, otherwise 0)

### Artifacts
[Artifacts Folder](https://github.com/AbdelhafidhMahouel/cintel-03-signal-design/tree/main/artifacts)

The dataset includes the new `high_error_flag` column along with the original signals, making it easier to identify high-error conditions.

### Insights
This project showed how derived signals can make system monitoring more effective. By adding the `high_error_flag`, I transformed a continuous metric into a clear indicator that highlights critical conditions.

This makes it easier to quickly identify abnormal behavior without manually analyzing raw values. It also improves decision-making by providing a simple and actionable signal.

---

## 4. Rolling Monitoring

### Repository Link
[View Repository](https://github.com/AbdelhafidhMahouel/cintel-04-rolling-monitoring)

### Techniques
- Applied rolling window calculations to smooth time-series data
- Used rolling means for requests, errors, and latency
- Added a new signal `requests_rolling_std` to measure variability over time

### Artifacts
[Artifacts Folder](https://github.com/AbdelhafidhMahouel/cintel-04-rolling-monitoring/tree/main/artifacts)

The output includes rolling averages along with the new rolling standard deviation signal for requests.

### Insights
This project showed that rolling averages help identify general trends, but they do not capture variability. By adding the `requests_rolling_std` signal, I was able to measure how much the system behavior fluctuates over time.

Higher standard deviation values indicate unstable or inconsistent system activity, while lower values indicate stable behavior. This provides deeper insight into system performance and helps detect spikes, sudden changes, or instability.

---

## 5. Drift Detection

### Repository Link
[View Repository](https://github.com/AbdelhafidhMahouel/cintel-05-drift-detection)

### Techniques
- Compared reference and current datasets to detect changes over time
- Calculated average values for key metrics (requests, errors, latency, error_rate)
- Added a new derived signal: error_rate for better system reliability analysis
- Created drift indicators including:
  - error_rate_difference between periods
  - individual drift flags for each metric
  - an overall drift flag combining all conditions

### Artifacts
[Artifacts Folder](https://github.com/AbdelhafidhMahouel/cintel-05-drift-detection/tree/main/artifacts)

The output includes additional columns such as `error_rate`, `error_rate_difference`, and drift flags that indicate whether the system behavior has changed.

### Insights
This project showed that drift detection becomes more powerful when combining multiple signals. By adding error_rate as a new metric, I was able to detect changes in system reliability, not just raw activity.

The overall drift flag simplifies interpretation by summarizing multiple conditions into a single indicator. This helps analysts quickly identify whether the system is stable or drifting and supports faster decision-making.

---

## 6. Continuous Intelligence Pipeline

### Repository Link
[View Repository](https://github.com/AbdelhafidhMahouel/cintel-06-continuous-intelligence)

### Techniques
- Combined multiple CI techniques into a single pipeline:
  - signal design (error_rate, avg_latency, success_rate, latency_per_error)
  - anomaly detection using thresholds
  - drift comparison between different periods
- Created a custom dataset and modified the pipeline logic
- Added validation checks and explanation labels for anomalies
- Implemented comparison between different time segments to analyze performance changes

### Artifacts
[Artifacts Folder](https://github.com/AbdelhafidhMahouel/cintel-06-continuous-intelligence/tree/main/artifacts)

The output includes enriched signals, anomaly flags, and additional information explaining system behavior and performance changes.

### Assessment
This project demonstrated how combining multiple monitoring techniques provides a complete view of system health. The pipeline not only detects anomalies but also explains why they occur and whether the system is improving or degrading over time.

By integrating signals, anomaly detection, and drift analysis, the system becomes more informative and supports better decision-making. This reflects how real-world continuous intelligence systems operate.
