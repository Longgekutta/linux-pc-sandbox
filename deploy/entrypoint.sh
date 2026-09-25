#!/usr/bin/env bash
set -e

echo "[Linux-PC-Sandbox] Initializing Virtual X11 Display :99 (${DISPLAY_WIDTH}x${DISPLAY_HEIGHT}x${DISPLAY_DEPTH})..."
Xvfb :99 -screen 0 ${DISPLAY_WIDTH}x${DISPLAY_HEIGHT}x${DISPLAY_DEPTH} -ac -nolisten tcp &
XVFB_PID=$!

# Wait for Xvfb socket
for i in {1..30}; do
    if [ -S /tmp/.X11-unix/X99 ]; then
        echo "[Linux-PC-Sandbox] Xvfb virtual display is ready on :99"
        break
    fi
    sleep 0.1
done

# Launch command
exec "$@"
