import time

import shuffle
import replace_items
import convert

PIPELINE = [
    (shuffle.main, 1),
    (replace_items.main, 3),
    (convert.main, 2),
]

def main():
    for func, delay in PIPELINE:
        print(f"\nRunning {func.__module__}...")

        func()  # <-- THIS is the key change

        print(f"Finished {func.__module__}")
        print(f"Waiting {delay} seconds...\n")

        time.sleep(delay)

    print("All scripts completed.")


if __name__ == "__main__":
    main()