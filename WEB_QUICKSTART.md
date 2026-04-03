# Advanced Reasoning System - Web Interface Quick Start

## 🚀 Launch the Web Interface

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Your API Key
```powershell
$env:DEEPSEEK_API_KEY = "your-deepseek-api-key-here"
```

### Step 3: Start the Web Server
```bash
python web_server.py
```

### Step 4: Open in Browser
Navigate to: **http://localhost:5000**

---

## 🎯 Using the Web Interface

### 1. **Enter Your Problem**
Type or paste your question/problem in the text area

### 2. **Upload Files (Optional)**
- Click the file upload area
- Select multiple files (.txt, .md, .py, .pdf, .json, .csv)
- Files will be attached as context

### 3. **Configure Settings**
- **Iterations:** Number of reasoning cycles (10-200)
  - 10-30: Quick problems (~10-30 seconds)
  - 50-80: Medium complexity (~1-2 minutes)
  - 100-200: Deep analysis (~2-5 minutes)

- **Advanced Settings** (optional):
  - Max Tree Depth: How deep reasoning tree grows
  - Branches per Node: Alternative approaches per step
  - Min Score: Pruning threshold

### 4. **Start Reasoning**
Click "🚀 Start Deep Reasoning" button

### 5. **Watch Progress**
Real-time updates showing:
- Progress percentage
- Current iteration
- Nodes explored
- Time elapsed
- Estimated time remaining

### 6. **View Results**
When complete:
- Solution displayed
- Statistics shown
- Log files available
- Start new problem or view logs

---

## 🎨 Features

✅ **Real-time Progress** - Live updates every second
✅ **File Upload** - Multiple files with drag-and-drop
✅ **Configurable** - Adjust all parameters via UI
✅ **Modern UI** - Dark theme, animations, responsive
✅ **Easy to Use** - No command line needed
✅ **Log Access** - Direct links to all log files

---

## 📊 Example Problems

### Simple Math
```
Problem: Solve x^2 - 4 = 0
Iterations: 20
```

### Code Analysis
```
Problem: Find bugs and optimization opportunities
Upload: your_code.py
Iterations: 50
```

### Proof
```
Problem: Prove that sqrt(2) is irrational
Iterations: 100
```

### Multi-File Analysis
```
Problem: Review this project for security issues
Upload: api.py, auth.py, database.py
Iterations: 80
```

---

## 🔧 Configuration Tips

**For Quick Tests:**
- Iterations: 10-20
- Time: ~10-20 seconds

**For Standard Problems:**
- Iterations: 50-80
- Time: ~30-60 seconds

**For Complex Analysis:**
- Iterations: 100-200
- Time: 1-5 minutes

---

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Check if port 5000 is in use
# Try different port:
python
>>> from web_server import run_server
>>> run_server(port=5001)
```

### Files Won't Upload
- Check file size (max 10MB)
- Check file type (see supported types)
- Check `uploads/` folder exists

### No Progress Updates
- Check browser console for errors
- Ensure JavaScript is enabled
- Try refreshing the page

### API Key Error
```powershell
# Make sure API key is set
$env:DEEPSEEK_API_KEY = "your-key"
python web_server.py
```

---

## 📁 File Structure

```
thinking/
├── web_server.py          # Flask server
├── templates/
│   └── index.html         # Web UI template
├── static/
│   ├── style.css          # Styling
│   └── script.js          # Frontend logic
└── uploads/               # Uploaded files (auto-created)
```

---

## 🌐 API Endpoints

If you want to integrate programmatically:

- `POST /api/start` - Start reasoning session
- `GET /api/progress/<session_id>` - Get progress
- `POST /api/upload` - Upload file
- `GET /api/config` - Get configuration

---

## 💡 Pro Tips

1. **Save Configurations** - Browser remembers your settings
2. **Multiple Tabs** - Can run multiple sessions
3. **File Organization** - Uploaded files saved in `uploads/`
4. **Log Access** - All logs in `logs/session_*/`
5. **Mobile Friendly** - Works on tablets and phones

---

## 🎯 Quick Start Commands

```bash
# Install
pip install -r requirements.txt

# Set API key
$env:DEEPSEEK_API_KEY = "your-key"

# Run server
python web_server.py

# Open browser
start http://localhost:5000
```

---

## ✨ What's Different from CLI?

| Feature | CLI | Web UI |
|---------|-----|--------|
| File Upload | Command line paths | Drag & drop |
| Progress | Text progress bar | Visual progress bar |
| Configuration | Edit config.py | UI controls |
| Results | Terminal output | Formatted display |
| Multiple Sessions | Sequential | Parallel |
| Ease of Use | Command line | Point & click |

---

**You're ready to go! Start the server and open http://localhost:5000** 🚀
