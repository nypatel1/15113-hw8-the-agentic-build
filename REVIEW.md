cat > /Users/nikeshpatel/15113-hw8-the-agentic-build/REVIEW.md << 'EOF'
# Code Review Against SPEC.md

## Acceptance Criteria Analysis

### 1. [FAIL] Weighted Question Selection Based on Feedback
**Location**: quiz_engine.py, line 17
**Issue**: Uses `random.choice()` without weighting. The spec requires that disliked questions appear less often and liked questions appear more often in future quizzes.
**Required Fix**: Implement weighted random selection using feedback scores from feedback.py. Questions should have selection probability proportional to their rating.

### 2. [FAIL] Hint Scoring (0.5 points instead of 1.0)
**Location**: quiz_engine.py, check_answer() method
**Issue**: No hint tracking or half-point scoring implemented. When a user requests a hint and answers correctly, they should receive 0.5 points, not 1.0.
**Required Fix**: Track hint usage per question in the quiz session, then apply 0.5x multiplier to score for questions where hints were used.

### 3. [FAIL] Invalid Answer Re-prompting Without Penalty
**Location**: quiz_engine.py, check_answer() method
**Issue**: No validation of answer format. For multiple choice questions, invalid inputs (like "X" when only A/B/C/D are valid) should trigger re-prompt, not count as wrong.
**Required Fix**: Validate answer against valid options before checking correctness. Loop until valid input received.

### 4. [FAIL] Category Filtering
**Location**: quiz_engine.py, no filter method exists
**Issue**: No mechanism to filter questions by category before quiz starts. Spec requires users to select a category and only see questions from that category.
**Required Fix**: Add category extraction from questions.json, present selection menu, filter question list accordingly.

### 5. [FAIL] User-Specific Stats Bar Chart
**Location**: stats.py, render_chart() or equivalent
**Issue**: No method to display ASCII bar chart. Even if it existed, no current_user parameter ensures chart only shows logged-in user's scores.
**Required Fix**: Implement ASCII bar chart rendering for last 10 quizzes; pass username to stats functions and enforce WHERE clause filtering.

---

## Additional Critical Issues

### Error Handling

### 6. [FAIL] Missing questions.json Validation
**Location**: quiz.py, quiz_engine.py - no validation logic
**Issue**: Spec requires friendly message and exit if questions.json is missing, malformed, or contains zero questions. Currently not implemented.
**Required Fix**: Add try/except for file loading and JSON parsing; validate questions array length; exit with appropriate code.

### 7. [FAIL] Missing Exit Code for Zero Questions
**Location**: Entire codebase
**Issue**: Spec specifies exit with code [not specified in excerpt] when no questions available. Current code has no exit code constants.
**Required Fix**: Define exit codes and use sys.exit() with proper codes for error conditions.

### 8. [FAIL] Missing Warning for Insufficient Questions After Filtering
**Location**: quiz_engine.py, no filtering implementation
**Issue**: If user filters by category and fewer questions exist than requested, app should warn and proceed with available questions.
**Required Fix**: After filtering, compare available vs. requested count and display warning if needed.

---

## Security Issues

### 9. [FAIL] Unsafe Password Hashing
**Location**: auth.py, line 13
**Issue**: Uses `hashlib.sha256()` directly instead of bcrypt. SHA256 is fast and vulnerable to rainbow table attacks. Passwords are not salted.
**Severity**: HIGH
**Required Fix**: Replace with bcrypt (listed in requirements.txt):
```python
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())