from pathlib import Path
import subprocess
import time

REARMP = Path("reARMP.exe")
ROOT = Path("GameData_Output")

# New output root
BIN_OUTPUT = Path("Bin_Output")
BIN_OUTPUT.mkdir(parents=True, exist_ok=True)

for json_file in ROOT.rglob("*.bin.json"):
    print(f"Processing: {json_file}")

    subprocess.run(
        [str(REARMP.resolve()), str(json_file.resolve())],
        cwd=ROOT,  # ensures reARMP writes output in ROOT
        check=True
    )

    # reARMP output always lands in ROOT
    output_file = ROOT / (json_file.name + ".bin")

    # Wait for file to appear
    timeout = 10
    start = time.time()

    while not output_file.exists():
        if time.time() - start > timeout:
            print(f"Timed out waiting for {output_file}")
            break
        time.sleep(0.25)

    if output_file.exists():
        # Preserve folder structure inside Bin_Output
        relative_path = json_file.relative_to(ROOT)
        final_file = BIN_OUTPUT / relative_path.with_suffix("")

        final_file.parent.mkdir(parents=True, exist_ok=True)

        if final_file.exists():
            final_file.unlink()

        output_file.rename(final_file)

        print(f"Moved to: {final_file}")

print("Done!")