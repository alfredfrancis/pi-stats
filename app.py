# main.py
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import platform
import psutil
import subprocess
import os
import time

app = FastAPI()

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SystemStats:
    def uptime(self):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        result = ""
        if days > 0:
            result += f"{days} day{'s' if days != 1 else ''}, "
        result += f"{hours} hour{'s' if hours != 1 else ''}, {minutes} minute{'s' if minutes != 1 else ''}"
        return result

    def temperature(self):
        try:
            # Try vcgencmd first (Raspberry Pi specific)
            temp = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
            return temp.replace('temp=', '').strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            try:
                # Try thermal_zone0 as fallback
                with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                    temp = float(int(f.read().strip()) / 1000)
                    return f"{temp}°C"
            except:
                return "N/A"

    def disk(self):
        disk = psutil.disk_usage('/')
        total_gb = disk.total / (1024**3)
        used_gb = disk.used / (1024**3)
        free_gb = disk.free / (1024**3)
        percent = disk.percent
        return f"{percent}% used ({used_gb:.1f}GB / {total_gb:.1f}GB)"

@app.get("/api/stats")
async def get_stats():
    stats_helper = SystemStats()
    stats = {
        "uptime": stats_helper.uptime(),
        "memory": f"{psutil.virtual_memory().percent}%",
        "cpu": f"{psutil.cpu_percent(interval=1)}%",
        "node": platform.node(),
        "system": platform.system(),
        "machine": platform.machine(),
        "architecture": f"{platform.architecture()[1]} {platform.architecture()[0]}",
        "temperature": stats_helper.temperature(),
        "disk": stats_helper.disk()
    }
    return stats

# Mount the static files directory
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)