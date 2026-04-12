# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Glossary** - project terms and concepts

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)

## Custom Project

### Dataset
The dataset used in this project is system_metrics_abdelhafidh.csv, which contains system performance data such as the number of requests, number of errors, and total latency in milliseconds. Each row represents one observation of system activity. This dataset is used to analyze system performance and detect potential issues.

### Signals
Several signals were created from the raw data to better understand system behavior. These include error rate, average latency, success rate, and latency per error. These signals help transform raw data into meaningful indicators that can be used to monitor system performance and detect anomalies.

### Experiments
I modified the original pipeline by creating my own version using a different input file and adding new logic. I introduced new signals such as success rate and latency per error, added validation for the data, and created labels to explain the reason behind anomalies. I also implemented a simple drift comparison between the first and second half of the dataset. These changes were made to improve the analysis and make the system more realistic.

### Results
After running the updated pipeline, I observed that the output became more detailed and informative. The system was able to identify anomalies more clearly and also explain why they occurred. The drift comparison provided additional insight into whether the system performance was improving or getting worse over time.

### Interpretation
These results show that adding more logic and signals improves the quality of the analysis. Instead of only detecting issues, the system now helps explain them and identify trends. As an analyst, this is important because it supports better decision-making and helps understand the overall health of the system.
