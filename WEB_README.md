# 🌐 Web Interface for Advanced Reasoning System

A modern, user-friendly web interface for the Advanced Reasoning System with real-time progress tracking, file uploads, and configurable settings.

![Web UI Screenshot](https://via.placeholder.com/800x400/0f172a/6366f1?text=Advanced+Reasoning+System+Web+UI)

## ✨ Features

- 🎨 **Modern Dark UI** - Beautiful gradient design with animations
- 📤 **File Upload** - Drag & drop multiple files
- ⚙️ **Configurable Settings** - Adjust all parameters via UI
- 📊 **Real-time Progress** - Live updates every second
- 📈 **Visual Statistics** - Iterations, nodes, time tracking
- 💾 **Results Display** - Formatted solution with statistics
- 📁 **Log Access** - Direct links to all log files
- 📱 **Responsive** - Works on desktop, tablet, and mobile

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
```powershell
# PowerShell
$env:DEEPSEEK_API_KEY = "your-deepseek-api-key"

# CMD
set DEEPSEEK_API_KEY=your-deepseek-api-key
```

### 3. Start Server

**Option A: Python**
```bash
python web_server.py
```

**Option B: Batch File (Windows)**
```bash
start_web.bat
```

**Option C: PowerShell**
```powershell
python web_server.py
```

### 4. Open Browser
Navigate to: **http://localhost:5000**

## 📖 How to Use

### Step 1: Enter Problem
Type your question or problem in the text area

### Step 2: Upload Files (Optional)
- Click upload area or drag files
- Supports: .txt, .md, .py, .pdf, .json, .csv
- Multiple files allowed
- Max 10MB per file

### Step 3: Configure
**Basic Settings:**
- **Iterations**: 10-200 (more = deeper thinking)

**Advanced Settings:**
- **Max Tree Depth**: 3-10
- **Branches per Node**: 2-5
- **Min Score**: 0.0-1.0

### Step 4: Start Reasoning
Click "🚀 Start Deep Reasoning"

### Step 5: Watch Progress
Real-time display shows:
- ⏱️ Progress percentage
- 🔄 Current iteration
- 🌳 Nodes explored
- ⏰ Elapsed/remaining time
- 💭 Status messages

### Step 6: View Results
- ✅ Solution text
- 📊 Statistics (score, time, nodes)
- 📁 Log file links
- 🔄 Start new problem

## 🎯 Example Use Cases

### Mathematical Problem
```
Problem: Solve the equation x^3 - 6x^2 + 11x - 6 = 0
Iterations: 50
Time: ~30 seconds
```

### Code Review
```
Problem: Review this code for bugs and optimizations
Files: example_code.py
Iterations: 60
Time: ~45 seconds
```

### Document Analysis
```
Problem: Summarize key findings from this research
Files: research.pdf
Iterations: 80
Time: ~1 minute
```

### Multi-File Project Review
```
Problem: Analyze this project architecture
Files: main.py, utils.py, config.py, README.md
Iterations: 100
Time: ~2 minutes
```

## 🔧 Server Configuration

### Default Settings
- Host: `0.0.0.0` (accessible from network)
- Port: `5000`
- Debug: `False` (production)

### Custom Port
```python
# In web_server.py at bottom:
if __name__ == '__main__':
    run_server(port=8080)  # Change port here
```

### Network Access
By default, server is accessible from your local network.
Find your IP and share: `http://YOUR_IP:5000`

## 📡 API Reference

### Start Session
```http
POST /api/start
Content-Type: application/json

{
  "problem": "Your problem here",
  "max_iterations": 50,
  "files": ["file1.txt", "file2.py"]
}

Response:
{
  "session_id": "20260216_112000_123456",
  "status": "started",
  "session_dir": "logs/session_20260216_112000"
}
```

### Get Progress
```http
GET /api/progress/<session_id>

Response:
{
  "progress": {
    "current_iteration": 25,
    "total_iterations": 50,
    "percentage": 50,
    "nodes_explored": 75,
    "status": "running",
    "elapsed_time": 15,
    "estimated_remaining": 15
  },
  "result": null,  // or result object when complete
  "error": null    // or error message if failed
}
```

### Upload File
```http
POST /api/upload
Content-Type: multipart/form-data

file: <binary>

Response:
{
  "filename": "example.txt",
  "size": 1024,
  "path": "uploads/example.txt"
}
```

### Get Configuration
```http
GET /api/config

Response:
{
  "min_thinking_time": 1800,
  "max_thinking_time": 3600,
  "max_iterations": 100,
  "supported_file_types": [".txt", ".md", ".py", ...]
}
```

## 🎨 UI Components

### Input Section
- Problem textarea
- File upload with drag & drop
- Configuration controls
- Advanced settings toggle

### Progress Section
- Animated progress bar
- Real-time statistics grid
- Status messages
- Time tracking

### Results Section
- Solution display
- Summary statistics
- Log file access
- Action buttons

## 🔒 Security Notes

⚠️ **Important Security Considerations:**

1. **API Key Protection**
   - Never commit API key to version control
   - Use environment variables
   - Don't expose in client-side code

2. **File Upload Validation**
   - File type checking implemented
   - Size limits enforced (10MB)
   - Files stored in isolated folder

3. **Network Access**
   - Default: Open to local network
   - Production: Use reverse proxy (nginx)
   - Consider: Add authentication

4. **CORS**
   - Currently: Permissive (CORS enabled)
   - Production: Restrict origins

## 🐛 Troubleshooting

### Server Won't Start

**Port Already in Use:**
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or use different port
python web_server.py  # Edit port in code
```

**Module Not Found:**
```bash
pip install -r requirements.txt
```

### File Upload Fails

**File Too Large:**
- Default limit: 10MB
- Solution: Compress or split file

**Unsupported Type:**
- Check supported: .txt, .md, .py, .pdf, .json, .csv
- Solution: Convert to supported format

**Uploads Folder Missing:**
```bash
mkdir uploads
```

### Progress Not Updating

**JavaScript Disabled:**
- Enable JavaScript in browser

**Console Errors:**
- Press F12
- Check Console tab
- Report errors

**Connection Issues:**
- Check server is running
- Verify URL: http://localhost:5000
- Check firewall settings

### No Results Displayed

**API Key Invalid:**
```powershell
# Verify API key is set
echo $env:DEEPSEEK_API_KEY

# Reset if needed
$env:DEEPSEEK_API_KEY = "correct-key"
```

**Check Logs:**
- View session folder
- Check `api_responses.log`
- Look for errors

## 📊 Performance

### Typical Performance
- **Iteration Rate**: ~2 iterations/second
- **File Upload**: Instant for files <1MB
- **Progress Updates**: Every 1 second
- **Memory Usage**: 200-500MB per session

### Optimization Tips
1. **Reduce iterations** for faster results
2. **Smaller files** upload faster
3. **Close unused sessions** to free memory
4. **Use Chrome/Edge** for best performance

## 🚀 Deployment

### Local Development
```bash
python web_server.py
```

### Production (nginx + gunicorn)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_server:app

# nginx config
server {
    listen 80;
    location / {
        proxy_pass http://localhost:5000;
    }
}
```

### Docker (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "web_server.py"]
```

## 📱 Mobile Support

The web interface is fully responsive:
- ✅ Touch-friendly controls
- ✅ Adaptive layouts
- ✅ Mobile file upload
- ✅ Works on iOS & Android

## 🎓 Advanced Usage

### Multiple Sessions
- Open multiple browser tabs
- Each tab = separate session
- Monitor different problems simultaneously

### Custom Styling
Edit `static/style.css`:
- Change colors (`:root` variables)
- Modify layouts
- Add custom animations

### API Integration
Use the REST API to integrate with other tools:
```python
import requests

# Start session
response = requests.post('http://localhost:5000/api/start', json={
    'problem': 'Solve x^2 = 4',
    'max_iterations': 30
})
session_id = response.json()['session_id']

# Poll for progress
while True:
    progress = requests.get(f'http://localhost:5000/api/progress/{session_id}')
    data = progress.json()
    if data['progress']['status'] == 'completed':
        print(data['result']['solution'])
        break
```

## 📚 Files Structure

```
thinking/
├── web_server.py           # Flask backend
├── templates/
│   └── index.html          # Main UI template
├── static/
│   ├── style.css           # Styling
│   └── script.js           # Frontend logic
├── uploads/                # Uploaded files
└── logs/                   # Session logs
    └── session_*/
        ├── final_result.txt
        ├── summary.txt
        ├── thought_tree.json
        ├── api_responses.log
        └── cas_computations.log
```

## ❓ FAQ

**Q: Can I run this on a server?**
A: Yes! Set host to `0.0.0.0` and share your IP address.

**Q: How many concurrent sessions?**
A: Unlimited, but each uses memory. Recommended: 3-5 max.

**Q: Can I customize the UI?**
A: Yes! Edit `static/style.css` and `templates/index.html`.

**Q: Is my data private?**
A: Files stored locally in `uploads/`. Logs in `logs/`. Not sent anywhere except DeepSeek API for reasoning.

**Q: Can I use without API key?**
A: No, DeepSeek API key is required for LLM functionality.

## 🆘 Support

- 📖 Read: `WEB_QUICKSTART.md`
- 📖 Read: `README.md`
- 🐛 Check: Browser console (F12)
- 📁 Check: Log files in `logs/`
- 🔍 Debug: `api_responses.log`

---

**Ready to use the web interface! Start the server and go!** 🚀

```bash
python web_server.py
# Open: http://localhost:5000
```
