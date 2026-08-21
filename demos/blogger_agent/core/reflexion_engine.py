"""
ReflexionEngine Primitive
Captures validation errors and build tracebacks, feeding them back to the LLM to self-heal content.
Logs full attempt details for rich terminal visibility.
"""

from collections.abc import Callable


class ReflexionEngine:
    def __init__(self, max_reflections: int = 3):
        self.max_reflections = max_reflections

    def execute_with_reflection(
        self,
        generation_fn: Callable[[str | None], str],
        validation_fn: Callable[[str], tuple[bool, str | None]],
    ) -> tuple[str, bool, int]:
        """
        Runs generation_fn and validates output with validation_fn.
        If validation fails, prints exact error to terminal and retries up to max_reflections.
        """
        feedback_prompt: str | None = None
        attempts = 0

        while attempts < self.max_reflections:
            attempts += 1
            print(f"--> Generation Attempt {attempts}/{self.max_reflections}...")

            output = generation_fn(feedback_prompt)
            is_valid, error_msg = validation_fn(output)

            if is_valid:
                print(f"    Attempt {attempts} PASSED validation!")
                return output, True, attempts

            print(f"    [Validation Failure] Attempt {attempts} FAILED: {error_msg}")

            # Construct reflection prompt for next attempt
            feedback_prompt = (
                f"Your previous output failed validation with the following error:\n"
                f"--- ERROR TRACEBACK ---\n{error_msg}\n-----------------------\n"
                f"Please analyze the error and regenerate the post to strictly correct this failure."
            )

        print(f"==> ReflexionEngine exhausted all {self.max_reflections} attempts.")
        return output, False, attempts
