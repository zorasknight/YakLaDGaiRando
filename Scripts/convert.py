from pathlib import Path
import subprocess
import time
from datetime import datetime
import shutil

REARMP = Path("reARMP.exe")
ROOT = Path("GameData_Output")
ASSETS = Path("Assets")

# Output folder
BIN_OUTPUT = Path(f"Gaiden_Rando")




def main():
    BIN_OUTPUT.mkdir(parents=True, exist_ok=True)

    for json_file in ROOT.rglob("*.bin.json"):
        print(f"Processing: {json_file}")

        subprocess.run(
            [str(REARMP.resolve()), str(json_file.resolve())],
            cwd=ROOT,
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

    # ZIP Output

    print("Creating zip archive...")

    # Copy metadata 
    shutil.copy2(ASSETS / "mod-image.ico", BIN_OUTPUT / "mod-image.ico")
    shutil.copy2(ASSETS / "mod-meta.yaml", BIN_OUTPUT / "mod-meta.yaml")
    shutil.copy2(ASSETS / "libcrypto-3-x64.dll", BIN_OUTPUT / "libcrypto-3-x64.dll")
    shutil.copy2(ASSETS / "libssl-3-x64.dll", BIN_OUTPUT / "libssl-3-x64.dll")
    shutil.copy2(ASSETS / "gaiden_hook_fresh.asi", BIN_OUTPUT / "gaiden_hook_fresh.asi")
    shutil.copy2(ASSETS / "item_mapping.csv", BIN_OUTPUT / "item_mapping.csv")
    

    zip_path = shutil.make_archive( base_name=str(BIN_OUTPUT), format="zip", root_dir=BIN_OUTPUT.parent, base_dir=BIN_OUTPUT.name, )

    print(f"Created archive: {zip_path}")

    # Cleanup (delete folder after completion)

    if Path(zip_path).exists():
        print("Deleting output folder...")
        shutil.rmtree(BIN_OUTPUT)
        print(f"Deleted folder: {BIN_OUTPUT}")
    else:
        print("Zip failed — folder not deleted.")


if __name__ == "__main__":
    main()