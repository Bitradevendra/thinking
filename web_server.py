"""
Web server for the Advanced Reasoning System
Provides a web UI for easy interaction
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import threading
import json
from datetime import datetime
from pathlib import Path
import time

from config import get_session_log_dir, MIN_THINKING_TIME, MAX_THINKING_TIME, TOT_MAX_ITERATIONS
from logger import ReasoningLogger
from llm_client import DeepSeekClient
from cas_solver import CASSolver
from tree_of_thoughts import TreeOfThoughts
from file_handler import FileInputHandler

app = Flask(__name__)
CORS(app)

# Global state for tracking active sessions
active_sessions = {}
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class WebReasoningSession:
    """Manages a web-based reasoning session"""
    
    def __init__(self, session_id):
        self.session_id = session_id
        self.progress = {
            'current_iteration': 0,
            'total_iterations': 0,
            'percentage': 0,
            'nodes_explored': 0,
            'status': 'initializing',
            'elapsed_time': 0,
            'estimated_remaining': 0
        }
        self.result = None
        self.error = None
        self.start_time = None
        
        try:
            self.session_dir = get_session_log_dir()
            self.logger = ReasoningLogger(self.session_dir)
            
            self.llm = DeepSeekClient(logger=self.logger)
            self.cas = CASSolver(logger=self.logger)
            self.file_handler = FileInputHandler()
            self.tot = TreeOfThoughts(self.llm, self.cas, self.logger)
            
            self.progress['status'] = 'ready'
        except Exception as e:
            self.error = f"Initialization error: {str(e)}"
            self.progress['status'] = 'error'
            import traceback
            print(f"Session initialization error: {traceback.format_exc()}")
        
    def update_progress(self, iteration, total, num_nodes):
        """Update progress information"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            rate = iteration / elapsed if elapsed > 0 else 0
            remaining = (total - iteration) / rate if rate > 0 else 0
        else:
            elapsed = 0
            remaining = 0
        
        self.progress.update({
            'current_iteration': iteration,
            'total_iterations': total,
            'percentage': int((iteration / total) * 100) if total > 0 else 0,
            'nodes_explored': num_nodes,
            'status': 'running',
            'elapsed_time': int(elapsed),
            'estimated_remaining': int(remaining)
        })
    
    def run_reasoning(self, problem, file_paths, max_iterations):
        """Run the reasoning process in background"""
        try:
            print(f"\n{'='*80}")
            print(f"RUN_REASONING METHOD CALLED:")
            print(f"{'='*80}")
            print(f"Problem text length RECEIVED: {len(problem)}")
            print(f"Problem first 200 chars: {problem[:200]}")
            print(f"File paths: {file_paths}")
            print(f"Max iterations: {max_iterations}")
            print(f"{'='*80}\n")
            
            self.progress['status'] = 'running'
            self.start_time = time.time()
            
            # Process files if any
            if file_paths:
                print(f"Processing {len(file_paths)} files...")
                file_context = self.file_handler.create_context_from_files(file_paths)
                print(f"File context length: {len(file_context)}")
                
                # LIMIT CONTEXT SIZE to prevent API errors (DeepSeek limit)
                MAX_CONTEXT_LEN = 20000  # Aggressive limit to ensure stability
                if len(file_context) > MAX_CONTEXT_LEN:
                    print(f"WARNING: File context too large ({len(file_context)} chars). Truncating to {MAX_CONTEXT_LEN}...")
                    file_context = file_context[:MAX_CONTEXT_LEN] + "\n\n[...CONTEXT TRUNCATED TO ENSURE STABILITY...]\n"
                
                # CRITICAL: Prepend file context but keep original problem
                full_problem = file_context + "\n\nPROBLEM:\n" + problem
                print(f"Full problem length (files + problem): {len(full_problem)}")
                print(f"Full problem starts with: {full_problem[:150]}")
                problem = full_problem
            else:
                print("No files to process, using problem text as-is")
            
            print(f"\nFinal problem text length: {len(problem)}")
            print(f"{'='*80}\n")
            
            # Run search
            result = self.tot.search(
                problem=problem,
                max_iterations=max_iterations,
                progress_callback=self.update_progress
            )
            
            # Save results
            self.logger.log_final_result(result)
            
            elapsed_time = time.time() - self.start_time
            stats = self.logger.get_stats()
            
            summary = f"""
Advanced Reasoning System - Session Summary
{'='*80}

Problem:
{problem[:500]}{'...' if len(problem) > 500 else ''}

Time Elapsed: {elapsed_time / 60:.1f} minutes
Total Iterations: {self.progress['current_iteration']}
Total Nodes: {stats['total_nodes']}
Branches Explored: {stats['branches_explored']}
Branches Pruned: {stats['branches_pruned']}
Best Score: {self.tot.best_score:.2f}

Best Solution Path:
{result}
"""
            self.logger.log_summary(summary)
            
            self.result = {
                'solution': result,
                'stats': stats,
                'elapsed_time': elapsed_time,
                'best_score': self.tot.best_score,
                'session_dir': self.session_dir
            }
            
            self.progress['status'] = 'completed'
            
        except Exception as e:
            self.error = str(e)
            self.progress['status'] = 'error'
            import traceback
            self.logger.log_final_result(f"Error: {e}\n\n{traceback.format_exc()}")


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/test')
def test_page():
    """Serve the test page for debugging"""
    return render_template('test.html')


@app.route('/api/start', methods=['POST'])
def start_reasoning():
    """Start a new reasoning session"""
    try:
        data = request.json
        print(f"\n{'='*80}")
        print(f"RECEIVED REQUEST DATA:")
        print(f"{'='*80}")
        print(f"Full JSON: {data}")
        print(f"{'='*80}\n")
        
        problem = data.get('problem', '')
        max_iterations = int(data.get('max_iterations', 50))
        uploaded_files = data.get('files', [])
        
        print(f"Extracted problem text (length={len(problem)}):")
        print(f"First 200 chars: {problem[:200]}")
        print(f"Max iterations: {max_iterations}")
        print(f"Files: {uploaded_files}")
        print(f"{'='*80}\n")
        
        if not problem or len(problem.strip()) == 0:
            print("ERROR: Problem text is empty!")
            return jsonify({'error': 'Problem text is required'}), 400
        
        # Create new session
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        print(f"Creating session: {session_id}")
        
        session = WebReasoningSession(session_id)
        
        # Check if session initialized correctly
        if session.error:
            return jsonify({'error': session.error}), 500
        
        active_sessions[session_id] = session
        print(f"Session added. Active sessions: {list(active_sessions.keys())}")
        
        # Process uploaded files
        file_paths = []
        if uploaded_files:
            for filename in uploaded_files:
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.exists(file_path):
                    file_paths.append(file_path)
        
        # Start reasoning in background thread
        thread = threading.Thread(
            target=session.run_reasoning,
            args=(problem, file_paths, max_iterations)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'session_id': session_id,
            'status': 'started',
            'session_dir': session.session_dir
        })
        
    except Exception as e:
        import traceback
        print(f"Start reasoning error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/progress/<session_id>')
def get_progress(session_id):
    """Get progress of a reasoning session"""
    print(f"Progress request for session: {session_id}")
    print(f"Active sessions: {list(active_sessions.keys())}")
    
    session = active_sessions.get(session_id)
    
    if not session:
        return jsonify({
            'error': 'Session not found',
            'requested_id': session_id,
            'active_sessions': list(active_sessions.keys())
        }), 404
    
    response = {
        'progress': session.progress,
        'result': session.result,
        'error': session.error
    }
    
    return jsonify(response)


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Get file info
        file_size = os.path.getsize(filepath)
        
        return jsonify({
            'filename': filename,
            'size': file_size,
            'path': filepath
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/config')
def get_config():
    """Get current configuration"""
    return jsonify({
        'min_thinking_time': MIN_THINKING_TIME,
        'max_thinking_time': MAX_THINKING_TIME,
        'max_iterations': TOT_MAX_ITERATIONS,
        'supported_file_types': ['.txt', '.md', '.py', '.pdf', '.json', '.csv']
    })


@app.route('/logs/<path:filepath>')
def serve_logs(filepath):
    """Serve log files"""
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    return send_from_directory(logs_dir, filepath)


def run_server(host='0.0.0.0', port=5000, debug=False):
    """Run the web server"""
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║   Advanced Reasoning System - Web Interface             ║
    ╚══════════════════════════════════════════════════════════╝
    
    Server running at: http://localhost:{port}
    
    Upload files, configure settings, and track progress in real-time!
    Press Ctrl+C to stop the server.
    """)
    
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == '__main__':
    run_server(debug=True)
