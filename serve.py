#!/usr/bin/env python3
"""
serve.py — drop-in replacement for `python3 -m http.server 8000`.
Serves the cockpit exactly like the stdlib server, but adds endpoints:

  POST /refresh   →  runs fetch_feed.py, returns {"ok": true, "output": "..."}
  GET  /pins      →  returns pins.json content
  POST /pins      →  body {"id":"...", "pinned":true/false, "story":{...}}
  GET  /dismissed →  returns history/dismissed.json (past removed stories)
"""
import json, subprocess, sys, threading, webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path

HERE = Path(__file__).parent
PORT = 8000
PINS_PATH = HERE / 'pins.json'
DISMISSED_PATH = HERE / 'history' / 'dismissed.json'

EMPTY_PINS = {"pinned_ids": [], "stories": {}}


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        if args and str(args[1]) not in ('200', '304'):
            super().log_message(fmt, *args)

    def _send_json(self, status, body_bytes):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body_bytes)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body_bytes)

    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/pins':
            body = PINS_PATH.read_bytes() if PINS_PATH.exists() else json.dumps(EMPTY_PINS).encode()
            self._send_json(200, body)
        elif path == '/dismissed':
            body = DISMISSED_PATH.read_bytes() if DISMISSED_PATH.exists() else b'[]'
            self._send_json(200, body)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/refresh':
            try:
                result = subprocess.run(
                    [sys.executable, str(HERE / 'fetch_feed.py')],
                    capture_output=True, text=True, timeout=60, cwd=str(HERE)
                )
                body = json.dumps({
                    'ok': result.returncode == 0,
                    'output': result.stdout + result.stderr,
                }).encode()
                self._send_json(200 if result.returncode == 0 else 500, body)
            except subprocess.TimeoutExpired:
                self._send_json(504, json.dumps({'ok': False, 'error': 'fetch timed out'}).encode())
            except Exception as e:
                self._send_json(500, json.dumps({'ok': False, 'error': str(e)}).encode())

        elif self.path == '/pins':
            try:
                length = int(self.headers.get('Content-Length', 0))
                req = json.loads(self.rfile.read(length))
                pins = json.loads(PINS_PATH.read_text()) if PINS_PATH.exists() else dict(EMPTY_PINS)
                # ensure stories key exists (schema migration)
                if 'stories' not in pins:
                    pins['stories'] = {}
                story_id = req['id']
                if req.get('pinned'):
                    if story_id not in pins['pinned_ids']:
                        pins['pinned_ids'].append(story_id)
                    if 'story' in req:
                        pins['stories'][story_id] = req['story']
                else:
                    pins['pinned_ids'] = [x for x in pins['pinned_ids'] if x != story_id]
                    pins['stories'].pop(story_id, None)
                PINS_PATH.write_text(json.dumps(pins, indent=2, ensure_ascii=False))
                self._send_json(200, json.dumps({'ok': True}).encode())
            except Exception as e:
                self._send_json(500, json.dumps({'ok': False, 'error': str(e)}).encode())

        elif self.path == '/generate':
            try:
                length = int(self.headers.get('Content-Length', 0))
                req = json.loads(self.rfile.read(length))
                story = req.get('story', {})
                component = req.get('component', 'script')

                pack_dir = HERE / 'content-engine' / 'packs' / 'wellness-genz'
                voice_dir = pack_dir / 'voice'
                fmt_dir = pack_dir / 'formats'

                def _r(p):
                    return p.read_text() if p.exists() else ''

                parts = [
                    'You are a short-form video content writer for a Gen Z wellness channel.',
                    'PACK CONTEXT:\n' + _r(pack_dir / 'pack.md'),
                    'VOICE BIBLE:\n' + _r(voice_dir / 'voice-bible.md'),
                    'VIDEO SCRIPT FORMAT:\n' + _r(fmt_dir / 'video-script.md'),
                ]
                if component in ('captions', 'package'):
                    parts.append('CAPTIONS FORMAT:\n' + _r(fmt_dir / 'captions.md'))
                examples_dir = voice_dir / 'examples'
                if examples_dir.exists():
                    examples = [p.read_text() for p in sorted(examples_dir.glob('*.md'))[:2]]
                    if examples:
                        parts.append('GOLD EXAMPLES (imitate their rhythm):\n' + '\n\n---\n\n'.join(examples))
                parts.append('Generate ONLY the requested component. No preamble, no commentary — deliver the output directly.')
                system = '\n\n'.join(filter(None, parts))

                srcs = story.get('sources', [])
                user_msg = (
                    f"Generate a {component} for this story.\n\n"
                    f"Headline: {story.get('headline', '')}\n"
                    f"Summary: {story.get('summary', '')}\n"
                    f"Source: {srcs[0]['outlet'] if srcs else 'Unknown'}\n"
                    f"URL: {srcs[0]['url'] if srcs else ''}\n"
                    f"Keywords: {', '.join(story.get('keyword_hits', []))}"
                )

                try:
                    import anthropic as _ant
                except ImportError:
                    self._send_json(500, json.dumps({'ok': False, 'error': 'Run: pip install anthropic'}).encode())
                    return

                client = _ant.Anthropic()
                msg = client.messages.create(
                    model='claude-sonnet-4-6',
                    max_tokens=1500,
                    system=system,
                    messages=[{'role': 'user', 'content': user_msg}],
                )
                content = msg.content[0].text
                self._send_json(200, json.dumps({'ok': True, 'content': content, 'component': component}).encode())

            except Exception as e:
                err = str(e)
                if any(k in err.lower() for k in ('api_key', 'authentication', 'x-api-key', 'invalid_api')):
                    err = 'ANTHROPIC_API_KEY not set — export it before starting serve.py'
                self._send_json(500, json.dumps({'ok': False, 'error': err}).encode())

        else:
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    import os
    os.chdir(HERE)
    url = f'http://localhost:{PORT}/cockpit.html'
    print(f'Cockpit → {url}  (Ctrl-C to stop)')
    threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    HTTPServer(('', PORT), Handler).serve_forever()
