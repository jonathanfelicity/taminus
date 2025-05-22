# actixpy/test_rust_bridge.py
try:
    import actixpy_core
    message = actixpy_core.rust_hello()
    print(f"Message from Rust: {message}")
    if message == "Hello from Rust via PyO3!":
        print("Successfully called Rust function from Python!")
    else:
        print(f"Unexpected message: {message}")
        exit(1)
except ImportError as e:
    print(f"Error importing actixpy_core: {e}")
    print("Make sure the Rust extension was built and installed correctly.")
    exit(1)
except AttributeError as e:
    print(f"Error calling function in actixpy_core: {e}")
    print("Make sure the 'rust_hello' function is correctly exposed in Rust.")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)
