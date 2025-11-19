#!/usr/bin/env python3
"""
Department of Living Memory (DoLM) Daemon
Watches files, captures errors, and maintains an Obsidian vault of all code issues.
"""

import os
import re
import sys
import time
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - DoLM - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DoLMConfig:
    """Configuration for DoLM daemon"""
    
    def __init__(self, config_path: str = None):
        self.vault_path = os.path.expanduser(
            os.getenv('DOLM_VAULT_PATH', '~/strategic-khaos-private/dolm-vault')
        )
        self.watch_extensions = ['.py', '.ps1', '.sh', '.js', '.rs', '.cpp', '.ts', '.jsx', '.tsx']
        self.watch_paths = [os.getenv('DOLM_WATCH_PATH', '/swarm')]
        self.error_patterns = [
            r'Error:.*',
            r'Exception:.*',
            r'Traceback.*',
            r'FATAL:.*',
            r'CRITICAL:.*',
            r'Segmentation fault.*',
            r'panic:.*',
        ]
        self.todo_patterns = [
            r'TODO:?\s*(.*)',
            r'FIXME:?\s*(.*)',
            r'HACK:?\s*(.*)',
            r'XXX:?\s*(.*)',
            r'BUG:?\s*(.*)',
            r'NOTE:?\s*(.*)',
        ]
        
        # Initialize vault structure
        self._init_vault()
    
    def _init_vault(self):
        """Initialize Obsidian vault directory structure"""
        vault = Path(self.vault_path)
        vault.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (vault / 'errors').mkdir(exist_ok=True)
        (vault / 'todos').mkdir(exist_ok=True)
        (vault / 'daily').mkdir(exist_ok=True)
        (vault / 'analytics').mkdir(exist_ok=True)
        
        # Create .obsidian config if it doesn't exist
        obsidian_dir = vault / '.obsidian'
        obsidian_dir.mkdir(exist_ok=True)
        
        # Create basic Obsidian config
        config = {
            "theme": "obsidian",
            "cssTheme": "",
            "baseFontSize": 16,
            "enabledPlugins": []
        }
        
        config_file = obsidian_dir / 'config.json'
        if not config_file.exists():
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
        
        logger.info(f"DoLM vault initialized at: {self.vault_path}")


class CodeAnalyzer:
    """Analyzes code files for errors and TODOs"""
    
    def __init__(self, config: DoLMConfig):
        self.config = config
        self.error_regex = [re.compile(p, re.IGNORECASE) for p in config.error_patterns]
        self.todo_regex = [re.compile(p, re.IGNORECASE) for p in config.todo_patterns]
    
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a file for errors and TODOs"""
        results = {
            'file': file_path,
            'timestamp': datetime.now().isoformat(),
            'todos': [],
            'errors': [],
            'stats': {}
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                # Check for TODOs
                for pattern in self.todo_regex:
                    match = pattern.search(line)
                    if match:
                        results['todos'].append({
                            'line': line_num,
                            'content': line.strip(),
                            'type': self._extract_todo_type(line),
                            'message': match.group(1) if match.lastindex else line.strip()
                        })
                
                # Check for error patterns (in comments or strings)
                for pattern in self.error_regex:
                    if pattern.search(line):
                        results['errors'].append({
                            'line': line_num,
                            'content': line.strip()
                        })
            
            results['stats'] = {
                'total_lines': len(lines),
                'todo_count': len(results['todos']),
                'error_count': len(results['errors'])
            }
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
        
        return results
    
    def _extract_todo_type(self, line: str) -> str:
        """Extract TODO type from line"""
        for keyword in ['TODO', 'FIXME', 'HACK', 'XXX', 'BUG', 'NOTE']:
            if keyword.lower() in line.lower():
                return keyword
        return 'TODO'


class ObsidianVault:
    """Manages Obsidian vault notes"""
    
    def __init__(self, config: DoLMConfig):
        self.config = config
        self.vault_path = Path(config.vault_path)
    
    def create_todo_note(self, todo_data: Dict, file_path: str):
        """Create or update a TODO note"""
        note_id = self._generate_note_id(file_path, todo_data['line'])
        note_path = self.vault_path / 'todos' / f"{note_id}.md"
        
        content = self._generate_todo_markdown(todo_data, file_path)
        
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.debug(f"Created TODO note: {note_path}")
    
    def create_error_note(self, error_data: Dict, file_path: str):
        """Create or update an error note"""
        note_id = self._generate_note_id(file_path, error_data['line'])
        note_path = self.vault_path / 'errors' / f"{note_id}.md"
        
        content = self._generate_error_markdown(error_data, file_path)
        
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.debug(f"Created error note: {note_path}")
    
    def create_daily_summary(self):
        """Create a daily summary note"""
        today = datetime.now().strftime('%Y-%m-%d')
        note_path = self.vault_path / 'daily' / f"{today}.md"
        
        # Count current TODOs and errors
        todo_count = len(list((self.vault_path / 'todos').glob('*.md')))
        error_count = len(list((self.vault_path / 'errors').glob('*.md')))
        
        content = f"""# DoLM Daily Summary - {today}

## Statistics
- **TODOs**: {todo_count}
- **Errors**: {error_count}
- **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Recent Activity
[[todos]] | [[errors]] | [[analytics]]

---
*Generated by Department of Living Memory*
*"Nothing is ever lost. Every error is a lesson. Every TODO is a prophecy."*
"""
        
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Created daily summary: {note_path}")
    
    def _generate_note_id(self, file_path: str, line_num: int) -> str:
        """Generate unique note ID from file path and line number"""
        data = f"{file_path}:{line_num}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def _generate_todo_markdown(self, todo_data: Dict, file_path: str) -> str:
        """Generate markdown content for TODO note"""
        todo_type = todo_data.get('type', 'TODO')
        message = todo_data.get('message', todo_data['content'])
        
        return f"""# {todo_type}: {message[:50]}

## Details
- **File**: `{file_path}`
- **Line**: {todo_data['line']}
- **Type**: {todo_type}
- **Discovered**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Content
```
{todo_data['content']}
```

## Context
File: [[{Path(file_path).name}]]

## Tags
#todo #{todo_type.lower()} #department-of-living-memory

---
*"Every TODO is a prophecy."*
"""
    
    def _generate_error_markdown(self, error_data: Dict, file_path: str) -> str:
        """Generate markdown content for error note"""
        return f"""# Error: {error_data['content'][:50]}

## Details
- **File**: `{file_path}`
- **Line**: {error_data['line']}
- **Captured**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Content
```
{error_data['content']}
```

## Analysis
- Review the context around line {error_data['line']}
- Check for similar patterns in related files
- Consider adding error handling

## Context
File: [[{Path(file_path).name}]]

## Tags
#error #needs-review #department-of-living-memory

---
*"Nothing is ever lost. Every error is a lesson."*
"""


class DoLMFileHandler(FileSystemEventHandler):
    """Handles file system events for DoLM"""
    
    def __init__(self, config: DoLMConfig, analyzer: CodeAnalyzer, vault: ObsidianVault):
        self.config = config
        self.analyzer = analyzer
        self.vault = vault
        self.processed_files: Set[str] = set()
    
    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return
        
        file_path = event.src_path
        
        # Check if file has a watched extension
        if not any(file_path.endswith(ext) for ext in self.config.watch_extensions):
            return
        
        # Avoid processing the same file too frequently
        if file_path in self.processed_files:
            return
        
        self.processed_files.add(file_path)
        
        # Process after a short delay to avoid partial writes
        time.sleep(0.5)
        
        logger.info(f"Processing file: {file_path}")
        self._process_file(file_path)
        
        # Remove from processed set after some time
        self.processed_files.discard(file_path)
    
    def _process_file(self, file_path: str):
        """Process a single file"""
        try:
            results = self.analyzer.analyze_file(file_path)
            
            # Create notes for TODOs
            for todo in results['todos']:
                self.vault.create_todo_note(todo, file_path)
            
            # Create notes for errors
            for error in results['errors']:
                self.vault.create_error_note(error, file_path)
            
            if results['todos'] or results['errors']:
                logger.info(
                    f"Found {results['stats']['todo_count']} TODOs and "
                    f"{results['stats']['error_count']} errors in {file_path}"
                )
        
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")


class DoLMDaemon:
    """Main DoLM daemon"""
    
    def __init__(self, config_path: str = None):
        self.config = DoLMConfig(config_path)
        self.analyzer = CodeAnalyzer(self.config)
        self.vault = ObsidianVault(self.config)
        self.observer = Observer()
    
    def start(self):
        """Start the DoLM daemon"""
        logger.info("=" * 60)
        logger.info("DEPARTMENT OF LIVING MEMORY (DoLM) - STARTING")
        logger.info("=" * 60)
        logger.info(f"Vault location: {self.config.vault_path}")
        logger.info(f"Watching: {', '.join(self.config.watch_paths)}")
        logger.info(f"File types: {', '.join(self.config.watch_extensions)}")
        logger.info("=" * 60)
        
        # Create initial daily summary
        self.vault.create_daily_summary()
        
        # Set up file system observer
        event_handler = DoLMFileHandler(self.config, self.analyzer, self.vault)
        
        for watch_path in self.config.watch_paths:
            if os.path.exists(watch_path):
                self.observer.schedule(event_handler, watch_path, recursive=True)
                logger.info(f"Watching: {watch_path}")
            else:
                logger.warning(f"Watch path does not exist: {watch_path}")
        
        # Initial scan of existing files
        logger.info("Performing initial scan...")
        self._initial_scan(event_handler)
        
        # Start observer
        self.observer.start()
        logger.info("DoLM daemon is now running. Press Ctrl+C to stop.")
        
        try:
            while True:
                time.sleep(3600)  # Update daily summary every hour
                self.vault.create_daily_summary()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the DoLM daemon"""
        logger.info("Stopping DoLM daemon...")
        self.observer.stop()
        self.observer.join()
        logger.info("DoLM daemon stopped.")
    
    def _initial_scan(self, handler: DoLMFileHandler):
        """Perform initial scan of all files"""
        file_count = 0
        
        for watch_path in self.config.watch_paths:
            if not os.path.exists(watch_path):
                continue
            
            for root, dirs, files in os.walk(watch_path):
                # Skip hidden directories and common ignore patterns
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]
                
                for file in files:
                    if any(file.endswith(ext) for ext in self.config.watch_extensions):
                        file_path = os.path.join(root, file)
                        handler._process_file(file_path)
                        file_count += 1
        
        logger.info(f"Initial scan complete. Processed {file_count} files.")


def main():
    """Main entry point"""
    logger.info("""
╔═══════════════════════════════════════════════════════════════╗
║   DEPARTMENT OF LIVING MEMORY (DoLM)                          ║
║   "Nothing is ever lost. Every error is a lesson.             ║
║    Every TODO is a prophecy."                                 ║
╚═══════════════════════════════════════════════════════════════╝
""")
    
    daemon = DoLMDaemon()
    daemon.start()


if __name__ == '__main__':
    main()
