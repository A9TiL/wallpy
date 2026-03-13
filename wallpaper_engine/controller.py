import subprocess
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PID_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine.pid")


def find_running_engine():
    result = subprocess.run(
        ["pgrep", "-f", "wallpaper_engine.core.static_engine"],
        capture_output=True,
        text=True
    )

    if result.stdout.strip():
        return int(result.stdout.strip().split("\n")[0])

    return None


def start_engine():

    pid = find_running_engine()

    if pid:
        print("Engine already running.")
        return

    process = subprocess.Popen(
        ["python3", "-m", "wallpaper_engine.core.static_engine"],
        cwd=PROJECT_ROOT
    )

    with open(PID_FILE, "w") as f:
        f.write(str(process.pid))

    print("Wallpaper engine started.")
    print("PID:", process.pid)


def stop_engine():

    pid = find_running_engine()

    if not pid:
        print("Engine not running.")
        return

    os.kill(pid, 9)

    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

    print("Engine stopped.")


def status_engine():

    pid = find_running_engine()

    if pid:
        print("Engine running with PID:", pid)
    else:
        print("Engine not running.")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python controller.py start|stop|status")
        sys.exit()

    command = sys.argv[1]

    if command == "start":
        start_engine()

    elif command == "stop":
        stop_engine()

    elif command == "status":
        status_engine()

    else:
        print("Invalid command.")
