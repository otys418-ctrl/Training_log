# S-RE Integration Plan (Phase 3)

**Document Version:** 1.0  
**Last Updated:** October 17, 2025  
**Status:** Planning Document for Phase 3

---

## Overview

This document outlines how the **S-RE (Workout Session & Reference Engine)** will integrate with both **P-MIS** and **L-DPS** in Phase 3. S-RE is the orchestration and presentation layer that brings the entire Progressive Overload Log system together.

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│                S-RE (Port TBD)                       │
│        Workout Session & Reference Engine            │
│         (Frontend + Orchestration Layer)             │
│                                                      │
└────────────┬────────────────────────────┬───────────┘
             │                            │
             │                            │
    ┌────────▼────────┐          ┌───────▼────────┐
    │                 │          │                │
    │  P-MIS (8000)   │          │  L-DPS (8001)  │
    │  Plan Service   │          │  Log Service   │
    │                 │          │                │
    └─────────────────┘          └────────────────┘
```

---

## User Flow: Logging a Set (PRD Section V)

### Step-by-Step Integration

#### 1. **User Opens App (S-RE Initialization)**
```
User Action: Opens app
S-RE: Initialize session, get user_id from auth (future feature)
```

#### 2. **User Starts Workout (S-RE → P-MIS)**
```
User Action: Starts workout session
S-RE: Determine current day (e.g., "Monday")

API Call:
  GET http://localhost:8000/api/v1/plans/{user_id}/Monday

P-MIS Response:
  {
    "day": "Monday",
    "target_body_parts": ["Chest", "Triceps"],
    "exercises": [
      {"name": "Bench Press", "sets": 3, "reps": 10},
      {"name": "Incline Press", "sets": 3, "reps": 12},
      ...
    ]
  }

S-RE: Display day's workout to-do list
```

#### 3. **User Selects Exercise (S-RE → L-DPS)**
```
User Action: Taps "Bench Press"
S-RE: Query for reference data (PRD F.5.0)

API Call:
  GET http://localhost:8001/api/v1/logs/{user_id}/Bench%20Press/latest-session

L-DPS Response (if previous session exists):
  {
    "user_id": "user_123",
    "exercise_name": "Bench Press",
    "session_timestamp": "2025-10-15T10:05:00Z",
    "sets": [
      {"set_number": 1, "weight_used": 60.0, "reps_completed": 10},
      {"set_number": 2, "weight_used": 60.0, "reps_completed": 10},
      {"set_number": 3, "weight_used": 60.0, "reps_completed": 10}
    ],
    "total_sets": 3
  }

L-DPS Response (if no previous session):
  404 - "No previous session found for Bench Press"

S-RE: Display reference data in UI
      - Show "Last Session: 3 sets of 60kg x 10 reps"
      - Suggest progressive overload (e.g., "Try 62.5kg or 11 reps")
```

#### 4. **User Performs Set 1**
```
User Action: Performs set 1
User Action: Logs weight (62.5kg) and reps (10)
S-RE: Validate input, prepare log entry
```

#### 5. **User Logs Set 1 (S-RE → L-DPS)**
```
User Action: Taps "Log Set"
S-RE: Create log entry

API Call:
  POST http://localhost:8001/api/v1/logs
  Body: {
    "user_id": "user_123",
    "exercise_name": "Bench Press",
    "set_number": 1,
    "weight_used": 62.5,
    "reps_completed": 10,
    "rpe": 7  // optional
  }

L-DPS Response:
  201 Created
  {
    "log_entry_id": "uuid-xxx",
    "user_id": "user_123",
    "exercise_name": "Bench Press",
    "timestamp": "2025-10-17T14:32:10.123Z",
    "set_number": 1,
    "weight_used": 62.5,
    "reps_completed": 10,
    "rpe": 7,
    "created_at": "2025-10-17T14:32:10.123Z"
  }

S-RE: Update UI
      - Show "✅ Set 1 Logged: 62.5kg x 10"
      - Enable "Start Set 2" button
      - Display progressive overload achievement (beat 60kg!)
```

#### 6. **Repeat for Sets 2, 3, ...**
```
Same flow as Step 4-5 for each subsequent set
```

---

## S-RE Technical Requirements

### Frontend Components (Suggested)

#### 1. **WorkoutListView**
- Fetches daily workout from P-MIS
- Displays exercise list
- Shows completion status per exercise

#### 2. **ExerciseDetailView**
- Shows reference data from L-DPS
- Provides input fields for weight/reps
- Displays progressive overload suggestions
- Logs sets to L-DPS

#### 3. **SetLogger Component**
- Input validation (weight, reps, optional fields)
- Submit button → POST to L-DPS
- Success/error handling
- Visual feedback for logged sets

#### 4. **ReferenceDisplay Component**
- Shows previous session data from L-DPS
- Highlights best set
- Calculates volume (sets × reps × weight)
- Provides progressive overload targets

---

## API Integration Points

### P-MIS Integration

#### Get Daily Workout
```typescript
// Example: React/TypeScript
async function getDailyWorkout(userId: string, day: string) {
  const response = await fetch(
    `http://localhost:8000/api/v1/plans/${userId}/${day}`
  );
  
  if (!response.ok) {
    if (response.status === 404) {
      // No plan found - redirect to plan upload
      return null;
    }
    throw new Error('Failed to fetch workout');
  }
  
  return await response.json();
}
```

### L-DPS Integration

#### Get Reference Data
```typescript
async function getLatestSession(
  userId: string,
  exerciseName: string
) {
  const encodedName = encodeURIComponent(exerciseName);
  const response = await fetch(
    `http://localhost:8001/api/v1/logs/${userId}/${encodedName}/latest-session`
  );
  
  if (response.status === 404) {
    // First time doing this exercise
    return null;
  }
  
  if (!response.ok) {
    throw new Error('Failed to fetch reference data');
  }
  
  return await response.json();
}
```

#### Log Set
```typescript
async function logSet(logData: LogEntryCreate) {
  const response = await fetch(
    'http://localhost:8001/api/v1/logs',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(logData)
    }
  );
  
  if (!response.ok) {
    throw new Error('Failed to log set');
  }
  
  return await response.json();
}
```

---

## Data Flow Diagrams

### Read Operations
```
S-RE wants daily workout:
  S-RE → P-MIS GET /plans/{user}/{day} → S-RE displays

S-RE wants reference data:
  S-RE → L-DPS GET /logs/{user}/{exercise}/latest-session → S-RE displays
```

### Write Operations
```
S-RE logs a set:
  S-RE → L-DPS POST /logs → L-DPS saves → S-RE confirms
```

### Critical Rule
**S-RE NEVER writes to P-MIS**. The plan is read-only from S-RE's perspective.

---

## Error Handling

### P-MIS Errors

| Error | Code | S-RE Response |
|-------|------|---------------|
| No plan found | 404 | Redirect to plan upload page |
| Invalid day | 400 | Show error message |
| Server error | 500 | Retry with exponential backoff |

### L-DPS Errors

| Error | Code | S-RE Response |
|-------|------|---------------|
| No previous session | 404 | Show "First time doing this exercise!" |
| Invalid data | 422 | Show validation errors inline |
| Server error | 500 | Allow retry, cache entry locally |

---

## State Management (Suggested)

### S-RE State Model
```typescript
interface WorkoutSessionState {
  userId: string;
  currentDay: string;
  plannedExercises: Exercise[];
  currentExercise: Exercise | null;
  referenceData: SessionReferenceResponse | null;
  loggedSets: LogEntry[];
  isLoading: boolean;
  error: string | null;
}
```

---

## Progressive Overload Logic (S-RE Responsibility)

### Algorithm for Suggesting Next Weight/Reps

```typescript
function suggestProgressiveOverload(
  lastSession: SessionReferenceResponse
): ProgressionSuggestion {
  // Find heaviest set from last session
  const heaviestSet = lastSession.sets.reduce((max, set) => 
    set.weight_used > max.weight_used ? set : max
  );
  
  // Strategy 1: Add weight (2.5kg plates)
  const nextWeight = heaviestSet.weight_used + 2.5;
  
  // Strategy 2: Add reps (if below 12 reps)
  const nextReps = heaviestSet.reps_completed < 12 
    ? heaviestSet.reps_completed + 1 
    : heaviestSet.reps_completed;
  
  return {
    weightProgression: {
      suggested: nextWeight,
      lastUsed: heaviestSet.weight_used,
      message: `Try ${nextWeight}kg (up from ${heaviestSet.weight_used}kg)`
    },
    repProgression: {
      suggested: nextReps,
      lastUsed: heaviestSet.reps_completed,
      message: `Try ${nextReps} reps (up from ${heaviestSet.reps_completed})`
    }
  };
}
```

---

## Offline Support (Future Enhancement)

### Strategy
1. Cache last known plan from P-MIS locally
2. Cache reference data from L-DPS locally
3. Queue log entries locally when offline
4. Sync queued entries when back online

### Implementation
```typescript
class OfflineQueue {
  private queue: LogEntryCreate[] = [];
  
  async queueLog(entry: LogEntryCreate) {
    this.queue.push(entry);
    await this.saveToLocalStorage();
  }
  
  async syncWhenOnline() {
    for (const entry of this.queue) {
      await logSet(entry);
    }
    this.queue = [];
    await this.saveToLocalStorage();
  }
}
```

---

## Testing Strategy for S-RE

### Integration Tests
1. **P-MIS Integration**: Can fetch daily workout
2. **L-DPS Integration**: Can fetch reference data
3. **L-DPS Integration**: Can log sets
4. **Error Handling**: Graceful degradation when services unavailable

### E2E Tests
1. Complete workout flow from plan to logged sets
2. Progressive overload calculation accuracy
3. Multiple exercises in single session

---

## Security Considerations

### Authentication (Phase 3+)
- Add JWT-based authentication to S-RE
- Pass auth token to P-MIS and L-DPS
- Both services validate tokens

### CORS Configuration
- P-MIS: Allow S-RE origin
- L-DPS: Allow S-RE origin
- Production: Restrict to specific domains

---

## Performance Optimization

### Caching Strategy
- Cache P-MIS plan for 24 hours (plan rarely changes)
- Cache L-DPS reference data for current session
- Clear cache when user explicitly refreshes

### Request Batching
- Consider batching multiple log entries if user logs offline
- Single request with array of log entries (future L-DPS feature)

---

## Deployment Considerations

### Development
```
P-MIS: localhost:8000
L-DPS: localhost:8001
S-RE: localhost:3000 (typical React dev server)
```

### Production
```
P-MIS: https://api.polog.app/pmis
L-DPS: https://api.polog.app/ldps
S-RE: https://polog.app
```

---

## Next Steps for Phase 3

1. **Choose Frontend Framework**: React, Vue, or Svelte
2. **Design UI/UX**: Wireframes for workout flow
3. **Implement Core Components**: Listed above
4. **Connect to P-MIS**: Fetch daily workouts
5. **Connect to L-DPS**: Fetch & log data
6. **Add Progressive Overload Logic**: Weight/rep suggestions
7. **Testing**: E2E tests for complete flow
8. **Deployment**: Bundle all three services

---

## Success Criteria

Phase 3 is complete when:
- [ ] User can view daily workout from P-MIS
- [ ] User can see previous performance from L-DPS
- [ ] User can log sets to L-DPS
- [ ] Progressive overload suggestions are accurate
- [ ] UI is intuitive and responsive
- [ ] Error handling is graceful
- [ ] All three services work together seamlessly

---

**Status:** ✅ Ready for Phase 3 Development  
**Estimated Phase 3 Duration:** 2-3 weeks  
**Primary Tech Decision:** Frontend framework choice
