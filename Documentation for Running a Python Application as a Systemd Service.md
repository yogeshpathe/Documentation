# Documentation for Running a Python Application as a Systemd Service

## Overview
This documentation explains how to configure and manage a Python application (`worker.py`) as a systemd service. The setup includes activating a virtual environment before running the application.

## Service File Configuration
The following systemd service file (`worker.service`) has been created:

```ini
[Unit]
Description=Python Application Service
After=network.target

[Service]
Type=simple
Environment="env=DEMO"
WorkingDirectory=/home/ubuntu/runner-valornet-backend-worker/_work/valornet-backend-worker/valornet-backend-worker
ExecStart=/bin/bash -c "source /home/ubuntu/venv/bin/activate && python worker.py"
Restart=always
RestartSec=5
User=ubuntu

[Install]
WantedBy=multi-user.target
```

### Key Features:
1. **Environment Variable**: Sets `env=DEMO` as an environment variable.
2. **Working Directory**: Specifies the location of the Python application.
3. **Virtual Environment Activation**: Activates the virtual environment located at `/home/ubuntu/venv` before running the `worker.py` script.
4. **Automatic Restarts**: Ensures the service restarts on failure.
5. **User Permissions**: Runs the service as the `ubuntu` user.

## Steps to Implement

### 1. Save the Service File
Save the above content as `/etc/systemd/system/worker.service`.

### 2. Reload Systemd Daemon
Reload the systemd manager configuration to recognize the new service file:
```bash
sudo systemctl daemon-reload
```

### 3. Enable the Service
Enable the service to start on boot:
```bash
sudo systemctl enable worker.service
```

### 4. Start the Service
Start the service manually:
```bash
sudo systemctl start worker.service
```

### 5. Check Service Status
Verify the status of the service:
```bash
sudo systemctl status worker.service
```

## Virtual Environment Setup
Ensure the virtual environment exists and is located at `/home/ubuntu/venv`. If not, create and configure it:

1. Create the virtual environment:
   ```bash
   python3 -m venv /home/ubuntu/venv
   ```

2. Activate the virtual environment:
   ```bash
   source /home/ubuntu/venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r /home/ubuntu/runner-valornet-backend-worker/_work/valornet-backend-worker/valornet-backend-worker/requirements.txt
   ```

## Updating the Service
To apply changes to the service file, reload the systemd daemon and restart the service:

1. Reload the daemon:
   ```bash
   sudo systemctl daemon-reload
   ```

2. Restart the service:
   ```bash
   sudo systemctl restart worker.service
   ```

## Debugging
- Check logs for the service using:
  ```bash
  journalctl -u worker.service
  ```
- Ensure the virtual environment path and `worker.py` script are correctly configured in the service file.

