# S-RE: Workout Session & Reference Engine

**Version:** 1.0.0  
**Port:** 5173 (development)  
**Status:** ✅ Fully Operational

---

## 📋 Overview

S-RE is the **frontend orchestration layer** for the Progressive Overload Log system. It provides the user interface for logging workouts and tracking progressive overload by integrating with P-MIS (workout plans) and L-DPS (performance logs).

### Key Features (PRD Compliance)

- ✅ **F.2.0:** Daily workout to-do list from P-MIS
- ✅ **F.3.0:** Real-time set logging to L-DPS  
- ✅ **F.5.0:** Progressive overload reference display (CRITICAL)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

Server starts at **http://localhost:5173**

### 3. Ensure Backend Services Running

- **P-MIS:** http://localhost:8000
- **L-DPS:** http://localhost:8001

---

## 📱 User Flow

1. View daily workout list (from P-MIS)
2. Select an exercise
3. View previous session performance (from L-DPS)
4. Get progressive overload suggestions
5. Log sets in real-time (to L-DPS)
6. Track progress

---

## 🎯 PRD Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| F.2.0 | Daily To-Do Generation | ✅ Complete |
| F.3.0 | Real-Time Logging | ✅ Complete |
| F.5.0 | Progressive Overload Reference | ✅ Complete |

---

**Full documentation:** See `/docs/S-RE_IMPLEMENTATION_PLAN.md`
