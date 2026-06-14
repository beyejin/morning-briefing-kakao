# Morning Briefing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python morning briefing app that can run locally or from GitHub Actions and send a KakaoTalk summary.

**Architecture:** Use a standard-library-first CLI with focused modules for config, weather, calendar, news, outfit recommendations, formatting, and Kakao delivery. Keep network functions thin and make deterministic behavior testable.

**Tech Stack:** Python 3.11+, `unittest`, GitHub Actions, OpenWeather API, RSS feeds, Google Calendar private ICS URL, Kakao Message API.

---

### Task 1: Core Tests

**Files:**
- Create: `tests/test_briefing_core.py`

- [x] **Step 1: Write failing tests** for outfit recommendation, ICS parsing, and Korean briefing formatting.
- [x] **Step 2: Run tests and verify they fail** because the package does not exist yet.

### Task 2: Core Implementation

**Files:**
- Create: `morning_briefing/__init__.py`
- Create: `morning_briefing/models.py`
- Create: `morning_briefing/outfit.py`
- Create: `morning_briefing/calendar.py`
- Create: `morning_briefing/formatter.py`

- [x] **Step 1: Implement minimal code** to satisfy the core tests.
- [x] **Step 2: Run tests and verify they pass.**

### Task 3: Integrations and CLI

**Files:**
- Create: `morning_briefing/config.py`
- Create: `morning_briefing/http.py`
- Create: `morning_briefing/weather.py`
- Create: `morning_briefing/news.py`
- Create: `morning_briefing/kakao.py`
- Create: `morning_briefing/main.py`

- [x] **Step 1: Add environment-backed config and network fetchers.**
- [x] **Step 2: Add CLI entrypoint with dry-run support.**

### Task 4: Automation and Docs

**Files:**
- Create: `.github/workflows/morning-briefing.yml`
- Create: `.env.example`
- Create: `README.md`
- Create: `.gitignore`

- [x] **Step 1: Add a scheduled GitHub Actions workflow.**
- [x] **Step 2: Document setup, secrets, local test, and Kakao token requirements.**
