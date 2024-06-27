#!/bin/bash
echo "starting turbovnc"
screen -dmS turbovnc bash -c 'VGL_DISPLAY=egl VGL_FPS=30 /opt/TurboVNC/bin/vncserver -depth 24 -noxstartup -securitytypes TLSNone,X509None,None 2>&1 | tee /tmp/vnc.log; read -p "Press any key to continue..."'
# wait for VNC to be running
for i in {1..10}; do
    if xdpyinfo -display :1 > /dev/null 2>&1; then
        break
    fi
    if [ $i -eq 10 ]; then
        echo "Failed to start TurboVNC server"
        exit 1
    fi
    sleep 1
done
echo "starting xfce4"
screen -dmS xfce4 bash -c 'DISPLAY=:1 /usr/bin/xfce4-session 2>&1 | tee /tmp/xfce4.log'
echo "starting novnc"
screen -dmS novnc bash -c '/usr/local/novnc/noVNC-1.4.0/utils/novnc_proxy --vnc localhost:5901 --listen 5801 2>&1 | tee /tmp/novnc.log'