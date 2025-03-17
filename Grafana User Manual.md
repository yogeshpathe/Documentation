# Grafana User Manual

## Introduction
This user manual will guide developers on how to use the Grafana dashboard to view logs for their applications in the Development and QA environments.

## Accessing the Grafana Dashboard
1. Open your web browser.
2. Go to the Grafana dashboard URL: `https://monitoring.cxhope.ai`
3. Log in with your credentials.
   - **Username**: Provided by the admin.
   - **Password**: Provided by the admin.
4. Click **Login** to access the dashboard.

## Navigating the Dashboard
1. After logging in, you will see the main dashboard.
2. Use the **left sidebar** to navigate between different sections:
   - **Dashboards**: View predefined dashboards.
   - **Explore**: Search logs and metrics.
   - **Alerts**: View active alerts.
   - **Settings**: Manage user preferences.

## Viewing Application Logs
1. Click on **Explore** from the left sidebar.
2. In the **Query Selector**, choose the data source:
   - Select **Loki** (for log monitoring).
3. Use the **Log Stream Selector** to filter logs:
   - Select the correct namespace (e.g., `development`, `qa`).
   - Select the application name (e.g., `my-app`).
4. Click **Run Query** to fetch logs.

## Filtering Logs
- Use the **time filter** at the top right to select a time range.
- Use **log level filters** (e.g., `error`, `warn`, `info`, `debug`).
- Add **search keywords** to refine logs (e.g., `exception`, `failed request`).

## Saving and Sharing Queries
1. After creating a query, click **Save Query** to reuse it later.
2. Click **Share** to generate a link for your team members.

## Setting Up Alerts
1. Go to **Alerts** from the left sidebar.
2. Click **Create New Alert**.
3. Define alert conditions (e.g., if error count > 10 in 5 minutes).
4. Set up **Notification Channels** (Email, Slack, etc.).
5. Click **Save** to activate the alert.

## Troubleshooting
- If logs are not loading, check the data source connection.
- Ensure you have selected the correct namespace and application.
- Try adjusting the time filter for better results.

## Support
For any issues, contact the admin at **support@cxhope.ai**.
