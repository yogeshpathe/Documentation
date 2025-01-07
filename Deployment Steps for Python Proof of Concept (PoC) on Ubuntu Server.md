# Deployment Steps for Python Proof of Concept (PoC) on Ubuntu Server

## Prerequisites
Ensure you have the following ready before proceeding:
- A Personal Access Token (PAT) for cloning the repository.
- Python installed on the server (preferably Python 3.8+).
- `nginx` installed and configured on the server.

---

## Step 1: Clone the Repository
1. Use the PAT to clone the repository to the server.
   ```bash
   git clone https://<your_repo_url>.git
   ```
   Replace `<your_repo_url>` with the actual repository URL.

2. Navigate to the project directory:
   ```bash
   cd <repository-name>
   ```

---

## Step 2: Create a Virtual Environment
1. Create a virtual environment for the project:
   ```bash
   python3 -m venv venv
   ```

2. Ensure the virtual environment is created in the project directory.

---

## Step 3: Activate the Virtual Environment and Install Dependencies
1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Install the required dependencies from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

---

## Step 4: Start the Server
1. Start the server using any free port (e.g., 8000):
   ```bash
   python3 app.py --port 8000
   ```
   Replace `app.py` with your application entry point if different.

2. Confirm the application is running by accessing it via `http://<server-ip>:8000`.

---

## Step 5: Configure Nginx as a Proxy Server
1. Create a new Nginx configuration file:
   ```bash
   sudo nano /etc/nginx/sites-available/multilingual-poc
   ```

2. Add the following configuration targeting the application port (e.g., 8000):
   ```nginx
   server {
       listen 80;
       server_name identity.cxhope.ai;

       location /multilingual-poc {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

3. Enable the configuration by creating a symbolic link:
   ```bash
   sudo ln -s /etc/nginx/sites-available/multilingual-poc /etc/nginx/sites-enabled/
   ```

4. Test the Nginx configuration:
   ```bash
   sudo nginx -t
   ```

5. Reload Nginx to apply the changes:
   ```bash
   sudo systemctl reload nginx
   ```

6. Access the application via `https://identity.cxhope.ai/multilingual-poc`.

---

## Notes
- Ensure the server has the required permissions to allow traffic on the configured ports.
- For a secure setup, configure SSL certificates using tools like Let’s Encrypt.

---

