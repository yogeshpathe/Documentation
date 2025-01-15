#######################################################################
# Dockerfile
#######################################################################
FROM mcr.microsoft.com/windows:20H2

# Set the working directory
WORKDIR C:/app

# Copy the entire project into the container
COPY . C:/app

# Install Node.js
RUN powershell -Command \
    "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
    Invoke-WebRequest -Uri https://nodejs.org/dist/v18.16.0/node-v18.16.0-x64.msi -OutFile C:\\nodejs.msi; \
    Start-Process msiexec.exe -ArgumentList '/i','C:\\nodejs.msi','/quiet','/norestart' -NoNewWindow -Wait; \
    Remove-Item -Force C:\\nodejs.msi"

# Install Visual C++ Redistributables
RUN powershell -Command \
    "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
    Invoke-WebRequest -Uri https://aka.ms/vs/17/release/vc_redist.x64.exe -OutFile C:\\vc_redist.x64.exe; \
    Start-Process C:\\vc_redist.x64.exe -ArgumentList '/install','/quiet','/norestart' -NoNewWindow -Wait; \
    Remove-Item -Force C:\\vc_redist.x64.exe"

# Install dependencies for SignallingWebServer
WORKDIR C:/app/WebServers/SignallingWebServer
RUN npm install

# Expose the required ports
EXPOSE 80
EXPOSE 8888
EXPOSE 3478/udp
EXPOSE 5349/udp

# Copy the entrypoint script
WORKDIR C:/app
COPY entrypoint.ps1 C:/app/entrypoint.ps1

# Use Bypass so scripts can run despite default PowerShell restrictions
ENTRYPOINT ["powershell", "-ExecutionPolicy", "Bypass", "-File", "C:\\app\\entrypoint.ps1"]
