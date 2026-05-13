# Ironman Training Tracker API

Backend system developed with **FastAPI** to centralize, clean, and analyze training data retrieved from the **Strava API**. This project is built as a technical foundation to support my preparation for a **full-distance triathlon on December 13th**.

## Current Features
- **Strava Integration:** Secure connection via OAuth2 to fetch recent athletic activities.
- **Data Sanitization:** Processing raw JSON into readable metrics (km conversion, pace calculation, etc.).
- **Robust Persistence:** Local storage using **SQLite** and **SQLAlchemy** (ORM).
- **Guaranteed Idempotency:** Duplicate validation via `strava_id` to ensure data integrity and accurate weekly totals.

## Tech Stack
- **Language:** Python 3.14
- **Framework:** FastAPI
- **Database:** SQLite / SQLAlchemy
- **Validation:** Pydantic
- **HTTP Client:** HTTPX (Async)

## Roadmap
- [ ] Phase 2: Implementation of cumulative metrics (Total kilometers per discipline).
- [ ] Phase 3: Advanced filtering by sport type (Swim/Bike/Run).
- [ ] Phase 4: Integration with an AI-driven system for performance tracking.

---
*Developed by Jose Ariel - Software Engineering Appasionate & Ironman Trainee.*