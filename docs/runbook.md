# Operational Runbook

Normal run:
1. Confirm client files are available in Bronze.
2. Run orchestration.
3. Review failed Databricks/ADF activities.
4. Review Quarantine volumes.
5. Verify Silver and Gold validations.
6. Verify Azure SQL row counts.
7. Refresh Power BI.

Failure handling:
- Preserve Bronze.
- Correct transformation/configuration defects and rerun.
- Do not edit Bronze to hide source-quality problems.
- Investigate sudden Quarantine spikes before publishing downstream data.
