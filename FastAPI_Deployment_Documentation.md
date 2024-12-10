
# FastAPI Deployment with GitHub Actions and Systemd

This documentation provides a step-by-step guide for deploying and managing a FastAPI application using GitHub Actions and `systemd` service management. It includes instructions for debugging and restarting the service.

---

## **1. Overview**

### **Components Used**
1. **FastAPI Application**: A Python-based web framework running on `uvicorn`.
2. **GitHub Actions**: For automated CI/CD pipeline.
3. **Systemd**: To manage the FastAPI application as a persistent service.

### **Workflow Summary**
- On a `push` to the main branch, GitHub Actions deploys the updated code.
- The `systemd` service is restarted to apply the changes.

---

## **2. Setting Up the FastAPI Application**

### **Systemd Service File**

Create a `systemd` service file to manage the FastAPI application:

```ini
[Unit]
Description=FastAPI Application
After=network.target

[Service]
User=<your-username>
WorkingDirectory=/path/to/your/project  # Replace with the path to your project
ExecStart=/usr/bin/python3 -m uvicorn src.server:server --host 0.0.0.0 --port 8005
Restart=always
Environment=env=DEMO  # Set environment variables here

[Install]
WantedBy=multi-user.target
```

### Steps to Set Up `systemd`:
1. Create the service file:
   ```bash
   sudo nano /etc/systemd/system/fastapi.service
   ```
2. Reload the `systemd` daemon:
   ```bash
   sudo systemctl daemon-reload
   ```
3. Start and enable the service:
   ```bash
   sudo systemctl start fastapi.service
   sudo systemctl enable fastapi.service
   ```

### Verify the Service:
Check if the service is active:
```bash
sudo systemctl status fastapi.service
```

---

## **3. GitHub Actions Workflow**

The following workflow automates the deployment process:

### **`deploy.yml`**

```yaml
name: Deploy FastAPI Application

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  deploy:
    runs-on: self-hosted

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.12

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Restart FastAPI Service
        run: |
          sudo systemctl restart fastapi.service
          sudo systemctl status fastapi.service
```

---

## **4. Debugging the Service**

### **Check the Logs**
To view logs for the FastAPI application:
```bash
sudo journalctl -u fastapi.service -e
```

### **Verify Running Processes**
Check if the process is running using `ps` or `pgrep`:
```bash
ps aux | grep "uvicorn src.server:server"
pgrep -f "uvicorn src.server:server"
```

### **Check Listening Ports**
Verify that the application is listening on port `8005`:
```bash
ss -tuln | grep 8005
```

### **Test the Application**
Use `curl` to test the application:
```bash
curl http://127.0.0.1:8005
```

---

## **5. Troubleshooting**

### **Common Issues**
1. **Service Fails to Start**:
   - Verify the Python path in the `ExecStart` directive.
   - Check for missing dependencies or incorrect imports.

2. **Environment Variables**:
   - Ensure the required environment variables are set in the service file.

3. **Application Logs**:
   - Inspect the logs using `journalctl` to identify runtime errors.

4. **Incorrect Project Path**:
   - Ensure the `WorkingDirectory` in the service file points to the correct project folder.

---

## **6. Best Practices**
- Use a virtual environment to manage dependencies.
- Always verify changes in a staging environment before deploying to production.
- Use `systemd` for reliable service management and automatic restarts.

---

## **7. References**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Systemd Documentation](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
