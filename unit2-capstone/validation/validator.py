def validate_qualitative(answer: str, chunks: list) -> dict:
    refused = "cannot find" in answer.lower() or "i don't know" in answer.lower()
    grounded = len(chunks) > 0 and not refused
    return {
        "is_grounded": grounded,
        "refused_to_answer": refused,
        "flag": not grounded,
        "warning": "Response may not be grounded in source documents" if not grounded else None
    }

def validate_quantitative(answer: str, sql: str, validation_status: str) -> dict:
    return {
        "sql_validated": validation_status == "PASSED",
        "sql_blocked": validation_status == "FAILED",
        "execution_error": validation_status == "ERROR",
        "flag": validation_status != "PASSED",
        "warning": f"SQL validation status: {validation_status}" if validation_status != "PASSED" else None
    }
