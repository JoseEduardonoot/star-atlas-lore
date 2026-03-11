"""Star Atlas Lore Wiki — Local Preview Server.

Usage: python tools/wiki_preview.py [--port 8002]

Syncs canon/ -> docs/, runs mkdocs build, and serves the static site.
"""
import http.server
import socketserver
import os
import subprocess
import sys
import shutil

PORT = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8002
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sync_files():
    """Sync canon/ -> docs/ using binary copy."""
    count = 0
    # Files to exclude from sync (hidden from wiki but kept in canon)
    exclude = {"species/crumon.md"}
    mappings = [
        ("canon/factions", "docs/factions"),
        ("canon/species", "docs/species"),
        ("canon/geography", "docs/geography"),
        ("canon/geography/sectors", "docs/geography/sectors"),
        ("canon/geography/worlds", "docs/geography/worlds"),
    ]
    for src_dir, dst_dir in mappings:
        src_path = os.path.join(ROOT, src_dir)
        dst_path = os.path.join(ROOT, dst_dir)
        if not os.path.isdir(src_path):
            continue
        os.makedirs(dst_path, exist_ok=True)
        category = src_dir.split("/", 1)[1]  # e.g. "species", "factions"
        for fname in os.listdir(src_path):
            if fname.endswith(".md"):
                rel = f"{category}/{fname}"
                if rel in exclude:
                    continue
                shutil.copy2(os.path.join(src_path, fname), os.path.join(dst_path, fname))
                count += 1
    return count


def build_site():
    """Run mkdocs build --clean."""
    site_dir = os.path.join(ROOT, "site")
    if os.path.isdir(site_dir):
        shutil.rmtree(site_dir)
    result = subprocess.run(
        ["mkdocs", "build", "--clean"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    for line in result.stderr.split("\n"):
        if "Documentation built" in line:
            print(f"  {line.strip()}")
    return result.returncode == 0


def serve(port):
    """Serve site/ on given port with proper UTF-8 headers."""
    os.chdir(os.path.join(ROOT, "site"))

    BASE_PATH = "/star-atlas-lore/"

    class UTF8Handler(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            # Strip the /star-atlas-lore/ prefix so files resolve correctly
            if path.startswith(BASE_PATH):
                path = "/" + path[len(BASE_PATH):]
            elif path == "/star-atlas-lore":
                path = "/"
            return super().translate_path(path)

        def end_headers(self):
            if self.path.endswith(('.html', '/')):
                self.send_header('Content-Type', 'text/html; charset=utf-8')
            super().end_headers()

        def log_message(self, fmt, *args):
            path = str(args[0]) if args else ""
            if not any(ext in path for ext in [".js", ".css", ".png", ".svg", ".woff", ".ttf"]):
                super().log_message(fmt, *args)

    with socketserver.TCPServer(("127.0.0.1", port), UTF8Handler) as httpd:
        print(f"\n  Wiki live at: http://127.0.0.1:{port}/star-atlas-lore/")
        print("  Press Ctrl+C to stop\n")
        httpd.serve_forever()


if __name__ == "__main__":
    print("\n=== Star Atlas Lore Wiki — Local Preview ===\n")

    build_only = "--build-only" in sys.argv

    print("[1/3] Syncing canon -> docs...")
    n = sync_files()
    print(f"  Synced {n} files")

    print("\n[2/3] Building site...")
    if not build_site():
        print("  Build completed with warnings (normal)")

    if build_only:
        print("\n  Build-only mode — skipping server.")
        sys.exit(0)

    print(f"\n[3/3] Serving on port {PORT}...")
    try:
        serve(PORT)
    except KeyboardInterrupt:
        print("\nStopped.")
    except OSError:
        print(f"\n  Port {PORT} in use. Try: python tools/wiki_preview.py --port {PORT+1}")
        sys.exit(1)
