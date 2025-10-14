"""
Admin Dashboard for MCP Server
Provides monitoring, cache management, and server control
"""

import os
import time
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from cache import cache, stats
from main import config

app = FastAPI(title="MCP Server Admin Dashboard", version="1.0.0")

# Templates
templates = Jinja2Templates(directory="templates")

# Create templates directory and basic template
os.makedirs("templates", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    # System stats
    system_stats = {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'memory_used': f"{psutil.virtual_memory().used / 1024 / 1024:.1f} MB",
        'memory_total': f"{psutil.virtual_memory().total / 1024 / 1024:.1f} MB",
        'uptime': str(timedelta(seconds=int(time.time() - psutil.boot_time())))
    }

    # Cache stats
    cache_stats = stats.get_stats()

    # API status
    api_status = {
        'jina': bool(config.jina_api_key),
        'gemini': bool(config.gemini_api_key),
        'deepl': bool(config.deepl_api_key)
    }

    # Recent activity (mock data for now)
    recent_activity = [
        {"timestamp": datetime.now().strftime("%H:%M:%S"), "action": "Cache hit", "details": "fetch request"},
        {"timestamp": (datetime.now() - timedelta(minutes=2)).strftime("%H:%M:%S"), "action": "API call", "details": "Jina search"},
        {"timestamp": (datetime.now() - timedelta(minutes=5)).strftime("%H:%M:%S"), "action": "Cache miss", "details": "translate request"},
    ]

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "system_stats": system_stats,
        "cache_stats": cache_stats,
        "api_status": api_status,
        "recent_activity": recent_activity,
        "title": "MCP Server Dashboard"
    })

@app.get("/api/stats")
async def get_stats():
    """API endpoint for statistics"""
    return {
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "uptime": int(time.time() - psutil.boot_time())
        },
        "cache": stats.get_stats(),
        "apis": {
            "jina": bool(config.jina_api_key),
            "gemini": bool(config.gemini_api_key),
            "deepl": bool(config.deepl_api_key)
        }
    }

@app.post("/api/cache/clear")
async def clear_cache():
    """Clear all cache entries"""
    success = cache.clear()
    if success:
        return {"message": "Cache cleared successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to clear cache")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Create basic HTML template
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stat-card h3 { margin-top: 0; color: #2c3e50; }
        .metric { font-size: 2em; font-weight: bold; color: #3498db; }
        .status-good { color: #27ae60; }
        .status-bad { color: #e74c3c; }
        .activity-list { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .activity-item { padding: 10px 0; border-bottom: 1px solid #eee; }
        .activity-item:last-child { border-bottom: none; }
        .btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 MCP Server Admin Dashboard</h1>
            <p>Monitor and manage your AI tools server</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <h3>System Resources</h3>
                <p>CPU: <span class="metric">{{ system_stats.cpu_percent }}%</span></p>
                <p>Memory: <span class="metric">{{ system_stats.memory_percent }}%</span></p>
                <p>Used: {{ system_stats.memory_used }} / {{ system_stats.memory_total }}</p>
                <p>Uptime: {{ system_stats.uptime }}</p>
            </div>

            <div class="stat-card">
                <h3>Cache Performance</h3>
                <p>Hits: <span class="metric">{{ cache_stats.hits }}</span></p>
                <p>Misses: <span class="metric">{{ cache_stats.misses }}</span></p>
                <p>Hit Rate: <span class="metric">{{ cache_stats.hit_rate }}</span></p>
                <p>Sets: {{ cache_stats.sets }}</p>
                <button class="btn" onclick="clearCache()">Clear Cache</button>
            </div>

            <div class="stat-card">
                <h3>API Status</h3>
                <p>Jina AI: <span class="metric {% if api_status.jina %}status-good{% else %}status-bad{% endif %}">
                    {% if api_status.jina %}✅{% else %}❌{% endif %}</span></p>
                <p>Gemini: <span class="metric {% if api_status.gemini %}status-good{% else %}status-bad{% endif %}">
                    {% if api_status.gemini %}✅{% else %}❌{% endif %}</span></p>
                <p>DeepL: <span class="metric {% if api_status.deepl %}status-good{% else %}status-bad{% endif %}">
                    {% if api_status.deepl %}✅{% else %}❌{% endif %}</span></p>
            </div>
        </div>

        <div class="activity-list">
            <h3>Recent Activity</h3>
            {% for activity in recent_activity %}
            <div class="activity-item">
                <strong>{{ activity.timestamp }}</strong> - {{ activity.action }}: {{ activity.details }}
            </div>
            {% endfor %}
        </div>
    </div>

    <script>
        async function clearCache() {
            try {
                const response = await fetch('/api/cache/clear', { method: 'POST' });
                const result = await response.json();
                alert(result.message);
                location.reload();
            } catch (error) {
                alert('Error clearing cache: ' + error.message);
            }
        }

        // Auto-refresh stats every 30 seconds
        setInterval(async () => {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                // Update stats dynamically if needed
                console.log('Stats updated:', data);
            } catch (error) {
                console.error('Error updating stats:', error);
            }
        }, 30000);
    </script>
</body>
</html>
"""

with open("templates/dashboard.html", "w") as f:
    f.write(dashboard_html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)