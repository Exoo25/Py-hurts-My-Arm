import sys

def run(code):
    try:
        exec(code)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        code = " ".join(sys.argv[1:])  # Join all arguments into a single string
        run(code)
    else:
        print("No code provided.")
