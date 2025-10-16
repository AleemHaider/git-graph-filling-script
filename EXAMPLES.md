# Usage Examples

Complete examples for common use cases of the GitHub Activity Generator.

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Advanced Examples](#advanced-examples)
3. [Real-World Scenarios](#real-world-scenarios)
4. [Custom Patterns](#custom-patterns)

---

## Basic Examples

### Example 1: Last 6 Months

Fill the last 6 months with moderate activity (weekdays only).

```bash
python3 github_activity_generator.py --days 180
```

**Expected Output:**
- ~90 active days (weekdays only)
- 1-5 commits per day
- ~200-300 total commits

---

### Example 2: Last Year

Fill the entire last year with activity.

```bash
python3 github_activity_generator.py --days 365
```

**Expected Output:**
- ~180 active days (weekdays only, 70% frequency)
- 1-5 commits per day
- ~400-700 total commits

---

### Example 3: Specific Date Range

Generate activity from January 2021 to October 2025.

```bash
python3 github_activity_generator.py \
  --start-date 2021-01-01 \
  --end-date 2025-10-14
```

**Expected Output:**
- ~1,200 active days
- 1-5 commits per day
- ~1,700+ total commits

---

## Advanced Examples

### Example 4: High Activity Pattern

Simulate a very active developer (90% of days, more commits).

```bash
python3 github_activity_generator.py \
  --days 365 \
  --min-commits 3 \
  --max-commits 10 \
  --frequency 0.9
```

**Expected Output:**
- ~230 active days
- 3-10 commits per day
- ~1,500-2,000 total commits

---

### Example 5: Light Activity Pattern

Simulate occasional contributor (30% of days, fewer commits).

```bash
python3 github_activity_generator.py \
  --days 365 \
  --min-commits 1 \
  --max-commits 2 \
  --frequency 0.3
```

**Expected Output:**
- ~55 active days
- 1-2 commits per day
- ~80-110 total commits

---

### Example 6: Include Weekends

Generate activity for all 7 days of the week.

```bash
python3 github_activity_generator.py \
  --days 180 \
  --include-weekends
```

**Expected Output:**
- ~125 active days (70% of all days)
- 1-5 commits per day
- ~350-500 total commits

---

### Example 7: Custom Repository Location

Generate in a specific directory.

```bash
python3 github_activity_generator.py \
  --days 365 \
  --repo-path ~/projects/my-activity \
  --repo-name my-github-activity
```

---

## Real-World Scenarios

### Scenario 1: New Graduate Building Portfolio

You graduated in 2023 and want to show consistent learning activity.

```bash
# Generate moderate activity from graduation to now
python3 github_activity_generator.py \
  --start-date 2023-06-01 \
  --end-date 2025-10-14 \
  --min-commits 1 \
  --max-commits 4 \
  --frequency 0.6
```

**Result:** Shows consistent but realistic learning pattern over 2+ years.

---

### Scenario 2: Career Changer (Learning Phase)

Switched careers in 2024 and started coding.

```bash
# Light activity at start, increasing over time
# First 6 months (learning)
python3 github_activity_generator.py \
  --start-date 2024-01-01 \
  --end-date 2024-06-30 \
  --min-commits 1 \
  --max-commits 2 \
  --frequency 0.4 \
  --repo-path ~/github-activity-early

# Then push, then generate more recent activity
python3 github_activity_generator.py \
  --start-date 2024-07-01 \
  --end-date 2025-10-14 \
  --min-commits 2 \
  --max-commits 5 \
  --frequency 0.7 \
  --repo-path ~/github-activity-recent
```

**Result:** Shows progression and growth in coding activity.

---

### Scenario 3: Part-Time Contributor

You contribute to projects but not every day.

```bash
python3 github_activity_generator.py \
  --days 730 \
  --min-commits 1 \
  --max-commits 3 \
  --frequency 0.4
```

**Result:** Sporadic but consistent contributions over 2 years.

---

### Scenario 4: Active Open Source Maintainer

Simulate heavy open source activity.

```bash
python3 github_activity_generator.py \
  --start-date 2022-01-01 \
  --end-date 2025-10-14 \
  --min-commits 5 \
  --max-commits 15 \
  --frequency 0.85 \
  --include-weekends
```

**Result:** Very active pattern with commits on most days including weekends.

---

## Custom Patterns

### Pattern 1: Weekday Worker

Strong activity Monday-Friday, none on weekends.

```bash
python3 github_activity_generator.py \
  --days 365 \
  --min-commits 3 \
  --max-commits 8 \
  --frequency 0.95
```

**Result:** Professional work pattern with consistent weekday commits.

---

### Pattern 2: Weekend Warrior

Mostly weekend activity (need custom modification).

```bash
# Note: Requires modifying script to invert weekend logic
# Or use --include-weekends with lower frequency
python3 github_activity_generator.py \
  --days 365 \
  --min-commits 5 \
  --max-commits 12 \
  --frequency 0.3 \
  --include-weekends
```

---

### Pattern 3: Sprint Pattern

Periods of intense activity followed by breaks.

```bash
# Generate multiple periods separately

# Sprint 1
python3 github_activity_generator.py \
  --start-date 2024-01-01 \
  --end-date 2024-02-29 \
  --min-commits 5 \
  --max-commits 10 \
  --frequency 0.9 \
  --repo-path ~/activity-sprint1

# Break (no commits)

# Sprint 2
python3 github_activity_generator.py \
  --start-date 2024-05-01 \
  --end-date 2024-06-30 \
  --min-commits 5 \
  --max-commits 10 \
  --frequency 0.9 \
  --repo-path ~/activity-sprint2
```

**Result:** Shows realistic sprint/rest patterns.

---

### Pattern 4: Gradual Increase

Start light, increase activity over time.

```bash
# Year 1 - Learning
python3 github_activity_generator.py \
  --start-date 2023-01-01 \
  --end-date 2023-12-31 \
  --min-commits 1 \
  --max-commits 2 \
  --frequency 0.4 \
  --repo-path ~/activity-year1

# Year 2 - Growing
python3 github_activity_generator.py \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --min-commits 2 \
  --max-commits 5 \
  --frequency 0.6 \
  --repo-path ~/activity-year2

# Year 3 - Expert
python3 github_activity_generator.py \
  --start-date 2025-01-01 \
  --end-date 2025-10-14 \
  --min-commits 3 \
  --max-commits 8 \
  --frequency 0.8 \
  --repo-path ~/activity-year3
```

**Result:** Shows natural progression and skill development.

---

## Quick Reference

| Use Case | Days | Min | Max | Freq | Weekends |
|----------|------|-----|-----|------|----------|
| Casual | 365 | 1 | 2 | 0.3 | No |
| Moderate | 365 | 1 | 5 | 0.7 | No |
| Active | 365 | 3 | 8 | 0.85 | No |
| Very Active | 365 | 5 | 15 | 0.95 | Yes |
| Learning | 180 | 1 | 3 | 0.5 | No |
| Professional | 365 | 2 | 6 | 0.9 | No |

---

## Tips for Realistic Patterns

1. **Skip weekends** - Most developers don't commit on weekends (default behavior)
2. **Use 60-80% frequency** - Nobody commits every single day
3. **Vary commit counts** - 1-5 is realistic, 10+ per day looks suspicious
4. **Match your timeline** - Don't show activity before you started coding
5. **Consider breaks** - Vacations, holidays, busy periods are normal
6. **Multiple repositories** - Spread activity across different projects

---

## After Generation

Once commits are generated, push to GitHub:

```bash
cd github-activity  # or your custom repo path

# Add remote
git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git

# Push
git branch -M main
git push -u origin main --force
```

Your contribution graph will update within 30-60 minutes.

---

**Remember:** Use this tool ethically and be transparent about your experience when it matters.
