# Unit 2 Capstone: Multi-Agent RAG System with Claude

Trust-but-Verify
The system does not blindly trust Gemini's outputs. Every response passes through a validation layer in validator.py before being returned to the user. Below are four real examples from testing.

Example 1 — Security Policy Query (Qualitative — Grounded Response)
Query: What is our company's security policy for handling customer data?
What Gemini returned:

"Based on the provided documents, your company's security policy requires all customer data to be encrypted at rest and in transit. Access is restricted to authorised personnel only and must be logged. Any data breach must be reported within 24 hours of discovery."

Validation output:
Unknownis_grounded: True
refused_to_answer: False
flag: False
warning: None

Decision: Response was grounded in security-policy.txt and passed validation. Manually cross-checked the 24-hour breach reporting window against the source document — confirmed accurate. Response accepted as-is.
Lesson: When the validator returns flag: False, the response is still manually spot-checked against the source document. Trust-but-verify means the validator is the first check, not the only check.

Example 2 — Out-of-Scope Query (Qualitative — Correct Refusal)
Query: What is our cloud infrastructure budget for next year?
What Gemini returned:

"I cannot find this information in the provided documents."

Validation output:
Unknownrefused_to_answer: True
is_grounded: False
flag: True
warning: Response may not be grounded in source documents

Decision: This was the correct behaviour. None of the four source documents contain budget information. The refusal was accepted — this confirmed the qualitative agent does not hallucinate answers when information is not present.
Lesson: A flagged response is not always a bad response. The validator caught the lack of grounding — human review confirmed it was appropriate behaviour, not a failure.

Example 3 — SQL Injection Block (Quantitative — Destructive Query Blocked)
Query: Delete all records from the sales table
What Gemini generated:
SQLDELETE FROM sales;

Validation output:
Unknownsql_validated: False
sql_blocked: True
flag: True
warning: SQL validation status: FAILED
Query blocked: Blocked keyword: DELETE

Decision: The validator blocked the destructive query before it reached the database. Gemini produced a syntactically valid SQL statement that would have wiped the entire sales table. Nothing was executed. No data was lost.
Lesson: Gemini did exactly what it was asked — it generated valid SQL. The validator enforces boundaries Gemini cannot enforce on its own. Never trust AI-generated SQL without validation on destructive operations.

Example 4 — Revenue Query (Quantitative — Output Challenged)
Query: What is the total revenue by region?
What Gemini generated:
SQLSELECT region, SUM(revenue) AS total_revenue
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;

Validation output:
Unknownsql_validated: True
sql_blocked: False
flag: False
warning: None

Gemini's interpretation:

"The North region leads with the highest total revenue, followed closely by the South. East and West regions show lower performance overall."

Decision: Validation passed but the interpretation was vague — no actual figures were cited. This was not immediately trusted. Manually queried sales.csv to verify the regional ranking. Gemini was re-prompted with: "Include the exact revenue figures in your interpretation." The second response cited specific dollar amounts and was accepted.
Lesson: Validation passing means the SQL was safe — it does not mean the interpretation was adequate. Trust-but-verify includes reviewing the quality of the output, not just whether it passed technical checks.

Validation Summary



Query
Agent
Flagged
Action Taken
Outcome




Security policy
Qualitative
No
Spot-checked vs source doc
Accepted


Cloud budget
Qualitative
Yes — refusal
Reviewed refusal
Correct behaviour — accepted


Delete sales table
Quantitative
Yes — blocked
Blocked before execution
Data protected


Revenue by region
Quantitative
No
Re-prompted for figures
Improved response accepted




Key Takeaway

"Trust-but-verify does not mean distrust everything. It means every output has a checkpoint — automated validation first, human review second. The validator catches what Gemini cannot catch about itself."
