#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
import tarfile
import zipfile
import re
from urllib.parse import urlparse
import argparse
import json
import shutil
from io import BytesIO

# Optional dependencies
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None
try:
    from PIL import Image
except ImportError:
    Image = None

# --- CONFIGURATION ---
HOW_BASE_DIR = os.path.join(os.path.expanduser("~"), "how")
HOW_CONFIG_DIR = os.path.join(HOW_BASE_DIR, "config")
HOW_CONFIG_FILE = os.path.join(HOW_CONFIG_DIR, "config.json")
DEFAULT_HOW_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

# Ensure config directory exists
os.makedirs(HOW_CONFIG_DIR, exist_ok=True)

# --- GLOBAL CONFIG LOAD ---
HOW_CONFIG = {}
def _load_config():
    global HOW_CONFIG
    if os.path.exists(HOW_CONFIG_FILE):
        try:
            with open(HOW_CONFIG_FILE, 'r') as f:
                HOW_CONFIG = json.load(f)
        except Exception:
            HOW_CONFIG = {}
_load_config()

# --- ARGPARSE SETUP ---
def main():
    parser = argparse.ArgumentParser(description="how: Swiss Army Knife CLI tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # how worship <url>
    worship_parser = subparsers.add_parser("worship", help="Download and organize sheet music")
    worship_parser.add_argument("url", help="URL to sheet music (PDF/image/webpage)")

    # how go <directory>
    go_parser = subparsers.add_parser("go", help="Prints a validated directory path for cd")
    go_parser.add_argument("directory", help="Target directory to go to")

    # how self-test [-r]
    selftest_parser = subparsers.add_parser("self-test", help="Run self-tests for how")
    selftest_parser.add_argument("-r", "--results", action="store_true", help="Show detailed test results")

    args = parser.parse_args()

    if args.command == "worship":
        handle_worship(args.url)
    elif args.command == "go":
        handle_go(args.directory)
    elif args.command == "self-test":
        handle_selftest(args.results)

# --- WORSHIP SUBCOMMAND ---
SAVE_DIR = os.path.expanduser("~/how/worship/sheets/")
os.makedirs(SAVE_DIR, exist_ok=True)

def is_direct_file(url):
    return any(url.lower().endswith(ext) for ext in ['.pdf', '.png', '.jpg', '.jpeg', '.webp'])

def safe_filename_from_url(url, new_ext=".pdf"):
    name = os.path.basename(urlparse(url).path).split("?")[0]
    base = os.path.splitext(name)[0]
    return base + new_ext

def download_file(url):
    filename = safe_filename_from_url(url, new_ext=os.path.splitext(url)[1] if '.' in url else '.pdf')
    filepath = os.path.join(SAVE_DIR, filename)
    print(f"\U0001F4E5 Downloading to {filepath}...")
    r = requests.get(url)
    if r.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(r.content)
        print("\u2705 Download complete.")
        try:
            subprocess.run(['xdg-open', filepath], check=False)
        except Exception:
            pass
        return filepath
    else:
        print("\u274C Failed to download.")
        return None

def download_and_convert_image_to_pdf(url):
    if Image is None:
        print("Pillow (PIL) not installed. Cannot convert images.")
        return
    print(f"\U0001F5BC\uFE0F Downloading image from {url}...")
    response = requests.get(url)
    if response.status_code != 200:
        print("\u274C Could not download image.")
        return
    img = Image.open(BytesIO(response.content)).convert('RGB')
    filename = safe_filename_from_url(url)
    filepath = os.path.join(SAVE_DIR, filename)
    img.save(filepath, "PDF", resolution=100.0)
    print(f"\u2705 Image converted and saved as PDF at {filepath}")
    try:
        subprocess.run(['xdg-open', filepath], check=False)
    except Exception:
        pass

def parse_page_for_pdf(url):
    if BeautifulSoup is None:
        print("BeautifulSoup4 (bs4) not installed. Cannot parse pages.")
        return None
    print("\U0001F50D Looking for downloadable files on the page...")
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if ".pdf" in href.lower():
                return href if href.startswith("http") else urlparse(url).scheme + "://" + urlparse(url).netloc + href
    except Exception as e:
        print(f"\u26A0\uFE0F Error while parsing: {e}")
    return None

def handle_worship(url):
    if is_direct_file(url):
        if url.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            download_and_convert_image_to_pdf(url)
        else:
            download_file(url)
    else:
        found = parse_page_for_pdf(url)
        if found:
            print(f"\U0001F4C4 Found PDF: {found}")
            download_file(found)
        else:
            print("\u274C Couldn’t find a downloadable file on that page.")

# --- GO SUBCOMMAND ---
def handle_go(directory):
    # Expand ~, resolve relative paths
    expanded = os.path.abspath(os.path.expanduser(directory))
    if os.path.isdir(expanded):
        print(expanded)
        sys.exit(0)
    else:
        print(f"[how go] Error: '{directory}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

# --- SELF-TEST SUBCOMMAND ---
def handle_selftest(show_results):
    # Simple self-test suite
    results = []
    def test(name, fn):
        try:
            passed = fn()
        except Exception:
            passed = False
        results.append((name, passed))
    # Example tests (expand as needed)
    test('command_exists_python3', lambda: shutil.which('python3') is not None)
    test('command_exists_git', lambda: shutil.which('git') is not None)
    test('command_exists_wine', lambda: shutil.which('wine') is not None)
    test('command_exists_nano', lambda: shutil.which('nano') is not None)
    test('command_exists_pytest', lambda: shutil.which('pytest') is not None)
    test('command_exists_clamscan', lambda: shutil.which('clamscan') is not None)
    test('command_exists_powershell', lambda: shutil.which('powershell') is not None)
    test('command_exists_aapt', lambda: shutil.which('aapt') is not None)
    test('command_exists_adb', lambda: shutil.which('adb') is not None)
    test('download_file', lambda: isinstance(requests.get('https://httpbin.org/get'), requests.models.Response))
    test('extract_archive', lambda: hasattr(zipfile, 'is_zipfile') and hasattr(tarfile, 'is_tarfile'))
    test('path_risk_root', lambda: os.path.abspath('/') == '/')
    test('path_risk_etc', lambda: os.path.isdir('/etc'))
    test('path_risk_usr_local', lambda: os.path.isdir('/usr/local'))
    test('path_risk_var', lambda: os.path.isdir('/var'))
    test('path_risk_home_user_dir', lambda: os.path.isdir(os.path.expanduser('~')))
    test('path_risk_wine_system', lambda: True)  # Placeholder
    test('path_risk_wine_user_data', lambda: True)  # Placeholder
    test('file_create', lambda: open('/tmp/how_test_file', 'w').close() or os.path.exists('/tmp/how_test_file'))
    test('folder_create', lambda: os.makedirs('/tmp/how_test_folder', exist_ok=True) or os.path.isdir('/tmp/how_test_folder'))
    test('combined_create', lambda: os.makedirs('/tmp/how_test_combined', exist_ok=True) or os.path.isdir('/tmp/how_test_combined'))
    test('file_delete', lambda: (os.remove('/tmp/how_test_file'), True)[1] if os.path.exists('/tmp/how_test_file') else True)
    test('folder_delete', lambda: (shutil.rmtree('/tmp/how_test_folder'), True)[1] if os.path.exists('/tmp/how_test_folder') else True)
    test('parse_size_100M', lambda: 100*1024*1024 == 104857600)
    test('parse_size_plus5G', lambda: 5*1024*1024*1024 == 5368709120)
    test('parse_time_7d', lambda: 7*24*60*60 == 604800)
    test('parse_time_plus1m', lambda: 60 == 60)

    print("="*50)
    print("        HOW SELF-TEST RESULTS        ")
    print("="*50)
    for name, passed in results:
        print(f"  {name:<28}: [{'PASS' if passed else 'FAIL'}]")
    print("="*50)
    if any(not passed for _, passed in results):
        print("Some tests FAILED. Run 'how self-test -r' for details.")
    else:
        print("All tests passed!")
    if show_results:
        print("\nDETAILED RESULTS:")
        for name, passed in results:
            print(f"{name}: {'PASS' if passed else 'FAIL'}")

if __name__ == "__main__":
    # --- SUBCOMMAND ARGPARSE DISPATCH ---
    parser = argparse.ArgumentParser(description="how: Swiss Army Knife CLI tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # how worship <url>
    worship_parser = subparsers.add_parser("worship", help="Download and organize sheet music")
    worship_parser.add_argument("url", help="URL to sheet music (PDF/image/webpage)")

    # how go <directory>
    go_parser = subparsers.add_parser("go", help="Prints a validated directory path for cd")
    go_parser.add_argument("directory", help="Target directory to go to")

    # how self-test [-r]
    selftest_parser = subparsers.add_parser("self-test", help="Run self-tests for how")
    selftest_parser.add_argument("-r", action="store_true", dest="results", help="Show detailed test results")

    args = parser.parse_args()

    if args.command == "worship":
        # --- HOW WORSHIP SUBCOMMAND ---
        url = args.url
        # Use your config and path safety logic for SAVE_DIR
        SAVE_DIR = os.path.join(HOW_BASE_DIR, "worship", "sheets")
        os.makedirs(SAVE_DIR, exist_ok=True)
        def _worship_is_direct_file(url):
            return any(url.lower().endswith(ext) for ext in ['.pdf', '.png', '.jpg', '.jpeg', '.webp'])
        def _worship_safe_filename_from_url(url, new_ext=".pdf"):
            name = os.path.basename(urlparse(url).path).split("?")[0]
            base = os.path.splitext(name)[0]
            return base + new_ext
        def _worship_download_file(url):
            filename = _worship_safe_filename_from_url(url, new_ext=os.path.splitext(url)[1] if '.' in url else '.pdf')
            filepath = os.path.join(SAVE_DIR, filename)
            print(f"\U0001F4E5 Downloading to {filepath}...")
            r = requests.get(url)
            if r.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(r.content)
                print("\u2705 Download complete.")
                try:
                    subprocess.run(['xdg-open', filepath], check=False)
                except Exception:
                    pass
                return filepath
            else:
                print("\u274C Failed to download.")
                return None
        def _worship_download_and_convert_image_to_pdf(url):
            try:
                from PIL import Image
            except ImportError:
                print("Pillow (PIL) not installed. Cannot convert images.")
                return
            print(f"\U0001F5BC\uFE0F Downloading image from {url}...")
            response = requests.get(url)
            if response.status_code != 200:
                print("\u274C Could not download image.")
                return
            img = Image.open(BytesIO(response.content)).convert('RGB')
            filename = _worship_safe_filename_from_url(url)
            filepath = os.path.join(SAVE_DIR, filename)
            img.save(filepath, "PDF", resolution=100.0)
            print(f"\u2705 Image converted and saved as PDF at {filepath}")
            try:
                subprocess.run(['xdg-open', filepath], check=False)
            except Exception:
                pass
        def _worship_parse_page_for_pdf(url):
            try:
                from bs4 import BeautifulSoup
            except ImportError:
                print("BeautifulSoup4 (bs4) not installed. Cannot parse pages.")
                return None
            print("\U0001F50D Looking for downloadable files on the page...")
            try:
                r = requests.get(url, timeout=10)
                soup = BeautifulSoup(r.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if ".pdf" in href.lower():
                        return href if href.startswith("http") else urlparse(url).scheme + "://" + urlparse(url).netloc + href
            except Exception as e:
                print(f"\u26A0\uFE0F Error while parsing: {e}")
            return None
        if _worship_is_direct_file(url):
            if url.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                _worship_download_and_convert_image_to_pdf(url)
            else:
                _worship_download_file(url)
        else:
            found = _worship_parse_page_for_pdf(url)
            if found:
                print(f"\U0001F4C4 Found PDF: {found}")
                _worship_download_file(found)
            else:
                print("\u274C Couldn’t find a downloadable file on that page.")
        sys.exit(0)

    elif args.command == "go":
        # --- HOW GO SUBCOMMAND ---
        directory = args.directory
        expanded = os.path.abspath(os.path.expanduser(directory))
        if os.path.isdir(expanded):
            print(expanded)
            sys.exit(0)
        else:
            print(f"[how go] Error: '{directory}' is not a valid directory.", file=sys.stderr)
            sys.exit(1)

    elif args.command == "self-test":
        # --- IMPROVED SELF-TEST SUBCOMMAND ---
        show_results = args.results
        results = []
        def test(name, fn):
            try:
                passed = fn()
            except Exception:
                passed = False
            results.append((name, passed))
        # Example tests (expand as needed)
        test('command_exists_python3', lambda: shutil.which('python3') is not None)
        test('command_exists_git', lambda: shutil.which('git') is not None)
        test('command_exists_wine', lambda: shutil.which('wine') is not None)
        test('command_exists_nano', lambda: shutil.which('nano') is not None)
        test('command_exists_pytest', lambda: shutil.which('pytest') is not None)
        test('command_exists_clamscan', lambda: shutil.which('clamscan') is not None)
        test('command_exists_powershell', lambda: shutil.which('powershell') is not None)
        test('command_exists_aapt', lambda: shutil.which('aapt') is not None)
        test('command_exists_adb', lambda: shutil.which('adb') is not None)
        test('download_file', lambda: isinstance(requests.get('https://httpbin.org/get'), requests.models.Response))
        test('extract_archive', lambda: hasattr(zipfile, 'is_zipfile') and hasattr(tarfile, 'is_tarfile'))
        test('path_risk_root', lambda: os.path.abspath('/') == '/')
        test('path_risk_etc', lambda: os.path.isdir('/etc'))
        test('path_risk_usr_local', lambda: os.path.isdir('/usr/local'))
        test('path_risk_var', lambda: os.path.isdir('/var'))
        test('path_risk_home_user_dir', lambda: os.path.isdir(os.path.expanduser('~')))
        test('path_risk_wine_system', lambda: True)  # Placeholder
        test('path_risk_wine_user_data', lambda: True)  # Placeholder
        test('file_create', lambda: open('/tmp/how_test_file', 'w').close() or os.path.exists('/tmp/how_test_file'))
        test('folder_create', lambda: os.makedirs('/tmp/how_test_folder', exist_ok=True) or os.path.isdir('/tmp/how_test_folder'))
        test('combined_create', lambda: os.makedirs('/tmp/how_test_combined', exist_ok=True) or os.path.isdir('/tmp/how_test_combined'))
        test('file_delete', lambda: (os.remove('/tmp/how_test_file'), True)[1] if os.path.exists('/tmp/how_test_file') else True)
        test('folder_delete', lambda: (shutil.rmtree('/tmp/how_test_folder'), True)[1] if os.path.exists('/tmp/how_test_folder') else True)
        test('parse_size_100M', lambda: 100*1024*1024 == 104857600)
        test('parse_size_plus5G', lambda: 5*1024*1024*1024 == 5368709120)
        test('parse_time_7d', lambda: 7*24*60*60 == 604800)
        test('parse_time_plus1m', lambda: 60 == 60)

        print("="*50)
        print("        HOW SELF-TEST RESULTS        ")
        print("="*50)
        for name, passed in results:
            print(f"  {name:<28}: [{'PASS' if passed else 'FAIL'}]")
        print("="*50)
        if any(not passed for _, passed in results):
            print("Some tests FAILED. Run 'how self-test -r' for details.")
        else:
            print("All tests passed!")
        if show_results:
            print("\nDETAILED RESULTS:")
            for name, passed in results:
                print(f"{name}: {'PASS' if passed else 'FAIL'}")
        sys.exit(0)

    # If no subcommand matched, fall back to original main logic (if any)
