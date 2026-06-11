import subprocess
import time
import sys

PIPELINE = [
    ("shuffle.py", 1),
    ("replace_items.py", 3),
    ("convert.py", 2),
]

for script, delay in PIPELINE:
    print(f"\nRunning {script}...")

    subprocess.run([sys.executable, script], check=True)

    print(f"Finished {script}")
    print(f"Waiting {delay} seconds...\n")

    time.sleep(delay)

print("All scripts completed.")