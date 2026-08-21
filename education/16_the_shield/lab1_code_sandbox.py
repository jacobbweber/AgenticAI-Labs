"""Reference solution. Moved from the old education/labs tree."""
import os
import subprocess
import sys
import tempfile
import time
from typing import Dict, Any

def execute_sandboxed_python(code_snippet: str, timeout_seconds: float = 5.0) -> Dict[str, Any]:
    """
    Executes Python code inside an isolated subprocess sandbox with:
    1. Isolated temporary directory workspace.
    2. Hard timeout enforcement.
    3. Stdout / Stderr capture.
    4. Exact exit code extraction.
    """
    print(f"\n[SANDBOX] Initializing isolated subprocess environment (Timeout: {timeout_seconds}s)...")
    
    # Create isolated temporary directory for file isolation
    with tempfile.TemporaryDirectory(prefix="agent_sandbox_") as temp_dir:
        script_path = os.path.join(temp_dir, "sandbox_script.py")
        
        # Write untrusted code to isolated script file
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code_snippet)

        start_time = time.time()
        
        try:
            # Spawn isolated subprocess with captured stdout/stderr in temp_dir
            process = subprocess.Popen(
                [sys.executable, script_path],
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Wait for execution with hard timeout enforcement
            stdout, stderr = process.communicate(timeout=timeout_seconds)
            duration = time.time() - start_time
            exit_code = process.returncode

            print(f"  [SANDBOX] Execution Finished in {duration:.2f}s | Exit Code: {exit_code}")
            return {
                "status": "COMPLETED" if exit_code == 0 else "FAILED",
                "exit_code": exit_code,
                "stdout": stdout.strip(),
                "stderr": stderr.strip(),
                "duration_seconds": round(duration, 2)
            }

        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate()
            duration = time.time() - start_time
            print(f"  [TIMEOUT] [SANDBOX ALERT] Timeout Exceeded ({timeout_seconds}s)! Subprocess Terminated.")

            return {
                "status": "TIMEOUT_EXCEEDED",
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Error: Execution exceeded timeout limit of {timeout_seconds} seconds.",
                "duration_seconds": round(duration, 2)
            }

if __name__ == "__main__":
    print("=== STARTING SUBPROCESS CODE EXECUTION SANDBOX LAB ===")

    # Test 1: Valid Code Execution
    print("\n--- TEST 1: Valid Code Execution ---")
    valid_code = "print('Calculating 15 * 3...'); result = 15 * 3; print(f'Result: {result}')"
    res1 = execute_sandboxed_python(valid_code)
    print(f"Sandbox Output:\n{res1}")

    # Test 2: Runtime Error Code Execution (Traceback Capture)
    print("\n--- TEST 2: Runtime Error Code Execution ---")
    error_code = "data = [1, 2, 3]; print(data[10])"  # IndexError
    res2 = execute_sandboxed_python(error_code)
    print(f"Sandbox Output:\n{res2}")

    # Test 3: Infinite Loop Code Execution (Timeout Enforcement)
    print("\n--- TEST 3: Infinite Loop Code Execution ---")
    infinite_loop_code = "import time\nprint('Starting infinite loop...');\nwhile True: time.sleep(0.1)"
    res3 = execute_sandboxed_python(infinite_loop_code, timeout_seconds=2.0)
    print(f"Sandbox Output:\n{res3}")
