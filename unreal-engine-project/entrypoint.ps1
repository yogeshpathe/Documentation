Write-Host "Starting Signalling Web Server with TURN..."
Start-Process -NoNewWindow powershell -ArgumentList (
    "-ExecutionPolicy Bypass",
    "-File C:\\app\\WebServers\\SignallingWebServer\\platform_scripts\\cmd\\Start_WithTURN_SignallingServer.ps1"
)

Write-Host "Waiting 10 seconds for the Signalling Server to initialize..."
Start-Sleep -Seconds 10

Write-Host "Starting Unreal Engine application..."

# Verify this path is correct and the file really exists here
Start-Process -NoNewWindow `
    -FilePath "C:\app\CXHopeDemo4.exe" `
    -ArgumentList (
      "-PixelStreamingIP=0.0.0.0",
      "-PixelStreamingPort=8888",
      "-PixelStreamingWebRTCEnabled=1",
      "-PixelStreamingEnableAudio=1",
      "-RenderOffScreen",
      "-AudioMixer"
    #   "-ResX=1280",
    #   "-ResY=720",
    #   "-ForceRes",
    #   "-nopause",
    #   "-nosplash"
    )

Write-Host "All processes started. Keeping container alive..."
while ($true) {
    Start-Sleep -Seconds 3600
}
