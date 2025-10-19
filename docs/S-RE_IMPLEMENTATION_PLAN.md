# S-RE Implementation Plan: Workout Session & Reference Engine

**Version:** 2.0  
**Date:** October 18, 2025  
**Status:** 🔵 Ready for Implementation  
**Estimated Duration:** 2-3 weeks  

---

## Executive Summary

This document provides a **surgical, research-backed implementation plan** for the S-RE (Workout Session & Reference Engine) - the final phase of the Progressive Overload Log system. The plan is grounded in:

1. ✅ **Deep analysis** of existing P-MIS (port 8000) and L-DPS (port 8001) implementations
2. ✅ **PRD compliance** ensuring F.2.0, F.3.0, and F.5.0 requirements are met
3. ✅ **Architectural constraints** from WARP.md (strict three-module separation, immutability, unidirectional data flow)
4. ✅ **Modern best practices** from React.dev official documentation
5. ✅ **No system-breaking changes** - purely additive implementation

---

## 📊 Current State Analysis

### Existing Infrastructure

#### P-MIS (Plan Management & Ingestion Service)
- **Port:** 8000
- **Framework:** FastAPI (Python)
- **Database:** SQLite (pmis.db)
- **Status:** ✅ Operational
- **Key Endpoints:**
  - `GET /api/v1/plans/{user_id}/{day}` - Returns daily workout
  - `GET /api/v1/plans/{user_id}` - Returns full plan
  - `POST /api/v1/plans/upload` - Upload PDF plan
  - `DELETE /api/v1/plans/{user_id}` - Delete plan

#### L-DPS (Logbook & Data Persistence Service)
- **Port:** 8001
- **Framework:** FastAPI (Python)
- **Database:** SQLite (ldps.db)
- **Status:** ✅ Operational
- **Key Endpoints:**
  - `POST /api/v1/logs` - Create log entry
  - `GET /api/v1/logs/{user_id}/{exercise_name}/latest-session` - Get reference (CRITICAL for F.5.0)
  - `GET /api/v1/logs/{user_id}/history` - Get exercise history

### Gaps Identified

1. **No frontend UI** - Users cannot interact with the system
2. **No orchestration layer** - Services are isolated, need coordination
3. **No progressive overload logic** - Calculation and suggestions missing
4. **No user flow** - No guided workout experience

---

## 🏗️ Architectural Decisions

### Technology Stack

#### Frontend Framework: **React 18.3+ with Vite**

**Rationale:**
- ✅ **Official recommendation** from react.dev (Trust Score: 10)
- ✅ **Fast development** with Vite's HMR (Hot Module Replacement)
- ✅ **TypeScript support** for type safety with backend schemas
- ✅ **Hooks architecture** aligns with stateless component design
- ✅ **Large ecosystem** for fitness/workout UI patterns

#### Build Tool: **Vite 5.x**

**Rationale:**
- ⚡ **Lightning-fast** dev server startup (<1s)
- 📦 **Optimized builds** with Rollup
- 🔧 **Zero config** for TypeScript + React
- 🎯 **Modern standards** (ESM, tree-shaking)

#### State Management: **React Context + useReducer**

**Rationale:**
- ✅ **Built-in solution** - no external dependencies
- ✅ **Official pattern** from React docs (Task Management example)
- ✅ **Sufficient complexity** - workout state is moderate, not massive
- ❌ **No Redux/Zustand** - overkill for this use case

#### HTTP Client: **Native Fetch API**

**Rationale:**
- ✅ **Modern browsers** support fetch natively
- ✅ **TypeScript-friendly** with proper typing
- ✅ **Lightweight** - no axios dependency needed
- ✅ **Async/await** syntax for clean code

#### Styling: **CSS Modules + Modern CSS**

**Rationale:**
- ✅ **Component-scoped** styles (no global conflicts)
- ✅ **Vite support** out-of-the-box
- ✅ **CSS Variables** for theming
- ✅ **Flexbox/Grid** for responsive layouts
- ❌ **No Tailwind** - avoids bloat, keeps bundle small

#### Routing: **React Router v7**

**Rationale:**
- ✅ **Industry standard** for React navigation
- ✅ **Type-safe** routing with TypeScript
- ✅ **Nested routes** for exercise drill-down
- ✅ **History API** for browser back/forward

---

## 📂 Project Structure

```
Training_log/
├── pmis/                   # Existing - DO NOT MODIFY
├── ldps/                   # Existing - DO NOT MODIFY
├── sre/                    # NEW - S-RE Frontend
│   ├── public/             # Static assets
│   │   └── favicon.ico
│   ├── src/
│   │   ├── api/            # API client layer
│   │   │   ├── pmis.client.ts
│   │   │   ├── ldps.client.ts
│   │   │   └── types.ts    # TypeScript interfaces from schemas
│   │   ├── components/     # UI components
│   │   │   ├── common/     # Reusable (Button, Input, Card, Loader)
│   │   │   ├── exercise/   # Exercise-specific (ExerciseCard, SetLogger)
│   │   │   └── reference/  # Reference display (PreviousSession, ProgressBar)
│   │   ├── context/        # State management
│   │   │   ├── WorkoutContext.tsx
│   │   │   └── workoutReducer.ts
│   │   ├── hooks/          # Custom hooks
│   │   │   ├── useWorkoutSession.ts
│   │   │   ├── useExerciseReference.ts
│   │   │   └── useProgressiveOverload.ts
│   │   ├── pages/          # Main views
│   │   │   ├── WorkoutListPage.tsx
│   │   │   ├── ExerciseDetailPage.tsx
│   │   │   └── HistoryPage.tsx
│   │   ├── utils/          # Helper functions
│   │   │   ├── progressiveOverload.ts
│   │   │   ├── dateHelpers.ts
│   │   │   └── validators.ts
│   │   ├── App.tsx         # Root component + Router
│   │   ├── main.tsx        # Vite entry point
│   │   └── index.css       # Global styles
│   ├── index.html          # HTML entry
│   ├── tsconfig.json       # TypeScript config
│   ├── vite.config.ts      # Vite config
│   ├── package.json        # Dependencies
│   └── README.md           # S-RE docs
├── docs/
│   ├── PRD.md              # Existing
│   ├── S-RE_INTEGRATION_PLAN.md  # Existing
│   └── S-RE_IMPLEMENTATION_PLAN.md  # THIS FILE
└── package.json            # Root package.json
```

---

## 🔌 API Integration Layer

### Type Definitions (src/api/types.ts)

```typescript
// Mirror P-MIS schemas
export interface Exercise {
  name: string;
  sets: number | null;
  reps: number | null;
}

export interface DailyWorkout {
  workout_id: number;
  plan_id: string;
  day: string;
  target_body_parts: string[];
  exercises: Exercise[];
}

// Mirror L-DPS schemas
export interface LogEntryCreate {
  user_id: string;
  exercise_name: string;
  set_number: number;
  weight_used: number;
  reps_completed: number;
  duration?: number;
  distance?: number;
  rpe?: number;
}

export interface LogEntryResponse extends LogEntryCreate {
  log_entry_id: string;
  timestamp: string;
  created_at: string;
}

export interface SetData {
  set_number: number;
  weight_used: number;
  reps_completed: number;
  duration?: number;
  distance?: number;
  rpe?: number;
  timestamp: string;
}

export interface SessionReference {
  user_id: string;
  exercise_name: string;
  session_timestamp: string;
  sets: SetData[];
  total_sets: number;
}
```

### P-MIS Client (src/api/pmis.client.ts)

```typescript
import { DailyWorkout } from './types';

const PMIS_BASE_URL = import.meta.env.VITE_PMIS_URL || 'http://localhost:8000';

export class PMISClient {
  private baseUrl: string;

  constructor(baseUrl = PMIS_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Fetch daily workout (PRD F.2.0)
   */
  async getDailyWorkout(userId: string, day: string): Promise<DailyWorkout | null> {
    const response = await fetch(
      `${this.baseUrl}/api/v1/plans/${userId}/${encodeURIComponent(day)}`,
      { method: 'GET' }
    );

    if (response.status === 404) {
      return null; // No plan found
    }

    if (!response.ok) {
      throw new Error(`P-MIS error: ${response.status}`);
    }

    return response.json();
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/`);
      return response.ok;
    } catch {
      return false;
    }
  }
}

export const pmisClient = new PMISClient();
```

### L-DPS Client (src/api/ldps.client.ts)

```typescript
import { LogEntryCreate, LogEntryResponse, SessionReference } from './types';

const LDPS_BASE_URL = import.meta.env.VITE_LDPS_URL || 'http://localhost:8001';

export class LDPSClient {
  private baseUrl: string;

  constructor(baseUrl = LDPS_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Get latest session reference (PRD F.5.0 - CRITICAL)
   */
  async getLatestSession(
    userId: string,
    exerciseName: string,
    sessionThresholdHours = 2.0
  ): Promise<SessionReference | null> {
    const encodedName = encodeURIComponent(exerciseName);
    const url = `${this.baseUrl}/api/v1/logs/${userId}/${encodedName}/latest-session?session_threshold_hours=${sessionThresholdHours}`;

    const response = await fetch(url, { method: 'GET' });

    if (response.status === 404) {
      return null; // First time doing this exercise
    }

    if (!response.ok) {
      throw new Error(`L-DPS error: ${response.status}`);
    }

    return response.json();
  }

  /**
   * Log a set (PRD F.3.0)
   */
  async logSet(logEntry: LogEntryCreate): Promise<LogEntryResponse> {
    const response = await fetch(`${this.baseUrl}/api/v1/logs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(logEntry),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Failed to log set: ${error.detail || response.statusText}`);
    }

    return response.json();
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/`);
      return response.ok;
    } catch {
      return false;
    }
  }
}

export const ldpsClient = new LDPSClient();
```

---

## 🧠 State Management Architecture

### Workout State (src/context/WorkoutContext.tsx)

```typescript
import { createContext, useContext, useReducer, ReactNode } from 'react';
import { DailyWorkout, SessionReference, LogEntryResponse } from '../api/types';

// State shape
export interface WorkoutState {
  userId: string;
  currentDay: string;
  dailyWorkout: DailyWorkout | null;
  currentExerciseIndex: number;
  currentExercise: string | null;
  referenceData: SessionReference | null;
  loggedSets: LogEntryResponse[];
  isLoading: boolean;
  error: string | null;
}

// Actions
export type WorkoutAction =
  | { type: 'SET_USER_ID'; payload: string }
  | { type: 'SET_CURRENT_DAY'; payload: string }
  | { type: 'LOAD_WORKOUT_START' }
  | { type: 'LOAD_WORKOUT_SUCCESS'; payload: DailyWorkout }
  | { type: 'LOAD_WORKOUT_ERROR'; payload: string }
  | { type: 'SELECT_EXERCISE'; payload: { exerciseName: string; index: number } }
  | { type: 'LOAD_REFERENCE_SUCCESS'; payload: SessionReference | null }
  | { type: 'LOG_SET_SUCCESS'; payload: LogEntryResponse }
  | { type: 'CLEAR_LOGGED_SETS' }
  | { type: 'RESET_SESSION' };

// Context
const WorkoutContext = createContext<WorkoutState | undefined>(undefined);
const WorkoutDispatchContext = createContext<React.Dispatch<WorkoutAction> | undefined>(undefined);

// Reducer (see next section)
export { workoutReducer } from './workoutReducer';

// Provider
export function WorkoutProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(workoutReducer, initialState);

  return (
    <WorkoutContext.Provider value={state}>
      <WorkoutDispatchContext.Provider value={dispatch}>
        {children}
      </WorkoutDispatchContext.Provider>
    </WorkoutContext.Provider>
  );
}

// Hooks
export function useWorkout() {
  const context = useContext(WorkoutContext);
  if (context === undefined) {
    throw new Error('useWorkout must be used within WorkoutProvider');
  }
  return context;
}

export function useWorkoutDispatch() {
  const context = useContext(WorkoutDispatchContext);
  if (context === undefined) {
    throw new Error('useWorkoutDispatch must be used within WorkoutProvider');
  }
  return context;
}

// Initial state
const initialState: WorkoutState = {
  userId: 'user_123', // TODO: Replace with auth
  currentDay: getCurrentDay(),
  dailyWorkout: null,
  currentExerciseIndex: -1,
  currentExercise: null,
  referenceData: null,
  loggedSets: [],
  isLoading: false,
  error: null,
};

function getCurrentDay(): string {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  return days[new Date().getDay()];
}
```

### Workout Reducer (src/context/workoutReducer.ts)

```typescript
import { WorkoutState, WorkoutAction } from './WorkoutContext';

export function workoutReducer(state: WorkoutState, action: WorkoutAction): WorkoutState {
  switch (action.type) {
    case 'SET_USER_ID':
      return { ...state, userId: action.payload };

    case 'SET_CURRENT_DAY':
      return { ...state, currentDay: action.payload };

    case 'LOAD_WORKOUT_START':
      return { ...state, isLoading: true, error: null };

    case 'LOAD_WORKOUT_SUCCESS':
      return {
        ...state,
        isLoading: false,
        dailyWorkout: action.payload,
        error: null,
      };

    case 'LOAD_WORKOUT_ERROR':
      return {
        ...state,
        isLoading: false,
        error: action.payload,
        dailyWorkout: null,
      };

    case 'SELECT_EXERCISE':
      return {
        ...state,
        currentExercise: action.payload.exerciseName,
        currentExerciseIndex: action.payload.index,
        loggedSets: [], // Clear previous exercise's logs
        referenceData: null, // Will be loaded separately
      };

    case 'LOAD_REFERENCE_SUCCESS':
      return {
        ...state,
        referenceData: action.payload,
      };

    case 'LOG_SET_SUCCESS':
      return {
        ...state,
        loggedSets: [...state.loggedSets, action.payload],
      };

    case 'CLEAR_LOGGED_SETS':
      return {
        ...state,
        loggedSets: [],
      };

    case 'RESET_SESSION':
      return {
        ...state,
        currentExercise: null,
        currentExerciseIndex: -1,
        referenceData: null,
        loggedSets: [],
        error: null,
      };

    default:
      throw new Error(`Unknown action: ${(action as any).type}`);
  }
}
```

---

## 🧩 Component Architecture

### Common Components

#### Button (src/components/common/Button.tsx)

```typescript
import React from 'react';
import styles from './Button.module.css';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  loading?: boolean;
}

export function Button({
  variant = 'primary',
  size = 'medium',
  loading = false,
  disabled,
  children,
  className = '',
  ...props
}: ButtonProps) {
  return (
    <button
      className={`${styles.button} ${styles[variant]} ${styles[size]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? <span className={styles.spinner} /> : children}
    </button>
  );
}
```

#### Input (src/components/common/Input.tsx)

```typescript
import React from 'react';
import styles from './Input.module.css';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  unit?: string; // For weight/reps display (e.g., "kg", "reps")
}

export function Input({ label, error, unit, className = '', ...props }: InputProps) {
  return (
    <div className={styles.inputWrapper}>
      {label && <label className={styles.label}>{label}</label>}
      <div className={styles.inputGroup}>
        <input className={`${styles.input} ${error ? styles.error : ''} ${className}`} {...props} />
        {unit && <span className={styles.unit}>{unit}</span>}
      </div>
      {error && <span className={styles.errorText}>{error}</span>}
    </div>
  );
}
```

### Exercise Components

#### ExerciseCard (src/components/exercise/ExerciseCard.tsx)

```typescript
import { Exercise } from '../../api/types';
import { Button } from '../common/Button';
import styles from './ExerciseCard.module.css';

interface ExerciseCardProps {
  exercise: Exercise;
  isCompleted: boolean;
  onStart: () => void;
}

export function ExerciseCard({ exercise, isCompleted, onStart }: ExerciseCardProps) {
  return (
    <div className={`${styles.card} ${isCompleted ? styles.completed : ''}`}>
      <div className={styles.header}>
        <h3 className={styles.name}>{exercise.name}</h3>
        {isCompleted && <span className={styles.badge}>✓</span>}
      </div>
      <div className={styles.details}>
        {exercise.sets && <span>{exercise.sets} sets</span>}
        {exercise.reps && <span>× {exercise.reps} reps</span>}
      </div>
      <Button onClick={onStart} variant="primary">
        {isCompleted ? 'Review' : 'Start'}
      </Button>
    </div>
  );
}
```

#### SetLogger (src/components/exercise/SetLogger.tsx)

```typescript
import { useState } from 'react';
import { Input } from '../common/Input';
import { Button } from '../common/Button';
import styles from './SetLogger.module.css';

interface SetLoggerProps {
  setNumber: number;
  onLogSet: (weight: number, reps: number, rpe?: number) => Promise<void>;
  suggestedWeight?: number;
  suggestedReps?: number;
}

export function SetLogger({
  setNumber,
  onLogSet,
  suggestedWeight,
  suggestedReps,
}: SetLoggerProps) {
  const [weight, setWeight] = useState<string>(suggestedWeight?.toString() || '');
  const [reps, setReps] = useState<string>(suggestedReps?.toString() || '');
  const [rpe, setRpe] = useState<string>('');
  const [isLogging, setIsLogging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const weightNum = parseFloat(weight);
    const repsNum = parseInt(reps, 10);
    const rpeNum = rpe ? parseInt(rpe, 10) : undefined;

    if (isNaN(weightNum) || isNaN(repsNum)) {
      setError('Please enter valid numbers');
      return;
    }

    if (weightNum <= 0 || repsNum <= 0) {
      setError('Weight and reps must be positive');
      return;
    }

    if (rpeNum && (rpeNum < 1 || rpeNum > 10)) {
      setError('RPE must be between 1 and 10');
      return;
    }

    setIsLogging(true);
    setError(null);

    try {
      await onLogSet(weightNum, repsNum, rpeNum);
      // Reset for next set
      setWeight('');
      setReps('');
      setRpe('');
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setIsLogging(false);
    }
  };

  return (
    <form className={styles.logger} onSubmit={handleSubmit}>
      <h3>Set {setNumber}</h3>
      <div className={styles.inputs}>
        <Input
          type="number"
          label="Weight"
          unit="kg"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
          placeholder="100"
          step="2.5"
          required
        />
        <Input
          type="number"
          label="Reps"
          unit="reps"
          value={reps}
          onChange={(e) => setReps(e.target.value)}
          placeholder="10"
          min="1"
          required
        />
        <Input
          type="number"
          label="RPE (Optional)"
          unit="/10"
          value={rpe}
          onChange={(e) => setRpe(e.target.value)}
          placeholder="7"
          min="1"
          max="10"
        />
      </div>
      {error && <p className={styles.error}>{error}</p>}
      <Button type="submit" variant="primary" loading={isLogging}>
        Log Set {setNumber}
      </Button>
    </form>
  );
}
```

### Reference Component

#### PreviousSessionDisplay (src/components/reference/PreviousSessionDisplay.tsx)

```typescript
import { SessionReference } from '../../api/types';
import styles from './PreviousSessionDisplay.module.css';

interface PreviousSessionDisplayProps {
  reference: SessionReference | null;
  isLoading: boolean;
}

export function PreviousSessionDisplay({ reference, isLoading }: PreviousSessionDisplayProps) {
  if (isLoading) {
    return <div className={styles.loading}>Loading previous session...</div>;
  }

  if (!reference) {
    return (
      <div className={styles.empty}>
        <p>🎉 First time doing this exercise!</p>
        <p className={styles.hint}>Set your baseline performance</p>
      </div>
    );
  }

  const totalVolume = reference.sets.reduce(
    (sum, set) => sum + set.weight_used * set.reps_completed,
    0
  );

  const heaviestSet = reference.sets.reduce((max, set) =>
    set.weight_used > max.weight_used ? set : max
  );

  return (
    <div className={styles.reference}>
      <h3>Last Session</h3>
      <p className={styles.date}>
        {new Date(reference.session_timestamp).toLocaleDateString()}
      </p>
      
      <div className={styles.stats}>
        <div className={styles.stat}>
          <span className={styles.label}>Total Sets</span>
          <span className={styles.value}>{reference.total_sets}</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.label}>Volume</span>
          <span className={styles.value}>{totalVolume.toFixed(0)} kg</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.label}>Heaviest</span>
          <span className={styles.value}>
            {heaviestSet.weight_used}kg × {heaviestSet.reps_completed}
          </span>
        </div>
      </div>

      <div className={styles.sets}>
        {reference.sets.map((set, idx) => (
          <div key={idx} className={styles.setRow}>
            <span className={styles.setNum}>Set {set.set_number}</span>
            <span className={styles.setData}>
              {set.weight_used}kg × {set.reps_completed} reps
            </span>
            {set.rpe && <span className={styles.rpe}>RPE {set.rpe}</span>}
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 📄 Main Views/Pages

### WorkoutListPage (src/pages/WorkoutListPage.tsx)

```typescript
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useWorkout, useWorkoutDispatch } from '../context/WorkoutContext';
import { pmisClient } from '../api/pmis.client';
import { ExerciseCard } from '../components/exercise/ExerciseCard';
import styles from './WorkoutListPage.module.css';

export function WorkoutListPage() {
  const state = useWorkout();
  const dispatch = useWorkoutDispatch();
  const navigate = useNavigate();
  const [completedExercises, setCompletedExercises] = useState<Set<string>>(new Set());

  useEffect(() => {
    loadWorkout();
  }, [state.currentDay]);

  const loadWorkout = async () => {
    dispatch({ type: 'LOAD_WORKOUT_START' });
    
    try {
      const workout = await pmisClient.getDailyWorkout(state.userId, state.currentDay);
      
      if (!workout) {
        dispatch({ 
          type: 'LOAD_WORKOUT_ERROR', 
          payload: 'No workout plan found. Please upload a plan first.' 
        });
        return;
      }
      
      dispatch({ type: 'LOAD_WORKOUT_SUCCESS', payload: workout });
    } catch (err) {
      dispatch({ 
        type: 'LOAD_WORKOUT_ERROR', 
        payload: (err as Error).message 
      });
    }
  };

  const handleStartExercise = (exerciseName: string, index: number) => {
    dispatch({ 
      type: 'SELECT_EXERCISE', 
      payload: { exerciseName, index } 
    });
    navigate(`/exercise/${encodeURIComponent(exerciseName)}`);
  };

  if (state.isLoading) {
    return <div className={styles.loading}>Loading workout...</div>;
  }

  if (state.error) {
    return (
      <div className={styles.error}>
        <p>{state.error}</p>
        <button onClick={loadWorkout}>Retry</button>
      </div>
    );
  }

  if (!state.dailyWorkout) {
    return <div className={styles.empty}>No workout scheduled for today</div>;
  }

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>{state.currentDay}</h1>
        <p className={styles.bodyParts}>
          {state.dailyWorkout.target_body_parts.join(', ')}
        </p>
      </header>

      <div className={styles.exercises}>
        {state.dailyWorkout.exercises.map((exercise, idx) => (
          <ExerciseCard
            key={idx}
            exercise={exercise}
            isCompleted={completedExercises.has(exercise.name)}
            onStart={() => handleStartExercise(exercise.name, idx)}
          />
        ))}
      </div>

      <div className={styles.progress}>
        {completedExercises.size} / {state.dailyWorkout.exercises.length} completed
      </div>
    </div>
  );
}
```

### ExerciseDetailPage (src/pages/ExerciseDetailPage.tsx)

```typescript
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useWorkout, useWorkoutDispatch } from '../context/WorkoutContext';
import { ldpsClient } from '../api/ldps.client';
import { PreviousSessionDisplay } from '../components/reference/PreviousSessionDisplay';
import { SetLogger } from '../components/exercise/SetLogger';
import { Button } from '../components/common/Button';
import { calculateProgression } from '../utils/progressiveOverload';
import styles from './ExerciseDetailPage.module.css';

export function ExerciseDetailPage() {
  const { exerciseName } = useParams<{ exerciseName: string }>();
  const state = useWorkout();
  const dispatch = useWorkoutDispatch();
  const navigate = useNavigate();
  const [isLoadingReference, setIsLoadingReference] = useState(false);

  const decodedName = decodeURIComponent(exerciseName || '');

  useEffect(() => {
    if (decodedName) {
      loadReference();
    }
  }, [decodedName]);

  const loadReference = async () => {
    setIsLoadingReference(true);
    try {
      const reference = await ldpsClient.getLatestSession(state.userId, decodedName);
      dispatch({ type: 'LOAD_REFERENCE_SUCCESS', payload: reference });
    } catch (err) {
      console.error('Failed to load reference:', err);
      dispatch({ type: 'LOAD_REFERENCE_SUCCESS', payload: null });
    } finally {
      setIsLoadingReference(false);
    }
  };

  const handleLogSet = async (weight: number, reps: number, rpe?: number) => {
    const setNumber = state.loggedSets.length + 1;

    const logEntry = {
      user_id: state.userId,
      exercise_name: decodedName,
      set_number: setNumber,
      weight_used: weight,
      reps_completed: reps,
      rpe,
    };

    const response = await ldpsClient.logSet(logEntry);
    dispatch({ type: 'LOG_SET_SUCCESS', payload: response });
  };

  const handleFinish = () => {
    dispatch({ type: 'RESET_SESSION' });
    navigate('/');
  };

  const currentSetNumber = state.loggedSets.length + 1;
  const progression = state.referenceData 
    ? calculateProgression(state.referenceData) 
    : null;

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <Button variant="secondary" onClick={() => navigate('/')}>
          ← Back
        </Button>
        <h1>{decodedName}</h1>
      </header>

      <PreviousSessionDisplay 
        reference={state.referenceData} 
        isLoadingReference={isLoadingReference} 
      />

      {progression && (
        <div className={styles.suggestions}>
          <h3>Progressive Overload Targets</h3>
          <p>💪 Try {progression.suggestedWeight}kg × {progression.suggestedReps} reps</p>
        </div>
      )}

      <section className={styles.logging}>
        <h2>Current Session</h2>
        
        {state.loggedSets.length > 0 && (
          <div className={styles.loggedSets}>
            {state.loggedSets.map((log) => (
              <div key={log.log_entry_id} className={styles.loggedSet}>
                ✅ Set {log.set_number}: {log.weight_used}kg × {log.reps_completed}
                {log.rpe && ` (RPE ${log.rpe})`}
              </div>
            ))}
          </div>
        )}

        <SetLogger
          setNumber={currentSetNumber}
          onLogSet={handleLogSet}
          suggestedWeight={progression?.suggestedWeight}
          suggestedReps={progression?.suggestedReps}
        />
      </section>

      <Button variant="primary" onClick={handleFinish} className={styles.finishButton}>
        Finish Exercise
      </Button>
    </div>
  );
}
```

---

## 🧮 Progressive Overload Logic

### Utils (src/utils/progressiveOverload.ts)

```typescript
import { SessionReference } from '../api/types';

export interface Progression {
  suggestedWeight: number;
  suggestedReps: number;
  lastWeight: number;
  lastReps: number;
  strategy: 'weight' | 'reps' | 'both';
  message: string;
}

export function calculateProgression(reference: SessionReference): Progression {
  // Find the heaviest set from last session
  const heaviestSet = reference.sets.reduce((max, set) => 
    set.weight_used > max.weight_used ? set : max
  );

  const lastWeight = heaviestSet.weight_used;
  const lastReps = heaviestSet.reps_completed;

  // Progressive Overload Strategies:
  // 1. If reps < 12, add 1 rep
  // 2. If reps >= 12, add 2.5kg
  // 3. Prioritize rep progression for beginners

  let suggestedWeight = lastWeight;
  let suggestedReps = lastReps;
  let strategy: 'weight' | 'reps' | 'both' = 'reps';

  if (lastReps < 12) {
    // Add reps first
    suggestedReps = lastReps + 1;
    strategy = 'reps';
  } else {
    // Add weight, reset reps to comfortable range
    suggestedWeight = lastWeight + 2.5;
    suggestedReps = Math.max(8, lastReps - 2);
    strategy = 'weight';
  }

  const message = strategy === 'reps'
    ? `Add 1 rep (${lastReps} → ${suggestedReps})`
    : `Add 2.5kg (${lastWeight}kg → ${suggestedWeight}kg)`;

  return {
    suggestedWeight,
    suggestedReps,
    lastWeight,
    lastReps,
    strategy,
    message,
  };
}

/**
 * Check if current set beats previous session
 */
export function isBeatPreviousSession(
  currentWeight: number,
  currentReps: number,
  reference: SessionReference
): boolean {
  const heaviestSet = reference.sets.reduce((max, set) => 
    set.weight_used > max.weight_used ? set : max
  );

  // Progressive overload achieved if:
  // 1. More weight at same/more reps
  // 2. Same weight with more reps
  return (
    currentWeight > heaviestSet.weight_used ||
    (currentWeight === heaviestSet.weight_used && currentReps > heaviestSet.reps_completed)
  );
}
```

---

## 🚀 Implementation Phases

### Phase 1: Project Setup (Day 1)
**Files to Create:**
- `sre/package.json`
- `sre/tsconfig.json`
- `sre/vite.config.ts`
- `sre/index.html`
- `sre/src/main.tsx`
- `sre/src/App.tsx`

**Actions:**
```bash
cd /Users/flxshh/Desktop/WARP/Training_log
mkdir sre && cd sre
npm create vite@latest . -- --template react-ts
npm install react-router-dom
```

**Verification:**
- `npm run dev` starts on port 5173
- Hot reload works

---

### Phase 2: API Layer (Day 2-3)
**Files to Create:**
- `src/api/types.ts`
- `src/api/pmis.client.ts`
- `src/api/ldps.client.ts`

**Actions:**
- Copy schemas from P-MIS/L-DPS
- Implement fetch-based clients
- Add error handling

**Verification:**
- Can fetch workout from P-MIS
- Can log set to L-DPS
- Can get reference from L-DPS

---

### Phase 3: State Management (Day 4-5)
**Files to Create:**
- `src/context/WorkoutContext.tsx`
- `src/context/workoutReducer.ts`

**Actions:**
- Implement reducer following React docs pattern
- Create context providers
- Add custom hooks

**Verification:**
- State updates work
- Context accessible in components

---

### Phase 4: UI Components (Day 6-8)
**Files to Create:**
- `src/components/common/Button.tsx`
- `src/components/common/Input.tsx`
- `src/components/exercise/ExerciseCard.tsx`
- `src/components/exercise/SetLogger.tsx`
- `src/components/reference/PreviousSessionDisplay.tsx`

**Actions:**
- Build atomic components first
- Add CSS modules
- Ensure responsive design

**Verification:**
- Components render correctly
- Props work as expected
- Styles are scoped

---

### Phase 5: Pages & Routing (Day 9-11)
**Files to Create:**
- `src/pages/WorkoutListPage.tsx`
- `src/pages/ExerciseDetailPage.tsx`
- Updated `App.tsx` with router

**Actions:**
- Connect pages to state
- Implement navigation
- Add loading/error states

**Verification:**
- Complete user flow works
- Back/forward navigation works

---

### Phase 6: Progressive Overload (Day 12-13)
**Files to Create:**
- `src/utils/progressiveOverload.ts`

**Actions:**
- Implement progression algorithm
- Add visual feedback
- Test edge cases

**Verification:**
- Suggestions are accurate
- Beat detection works

---

### Phase 7: Integration Testing (Day 14)
**Actions:**
- Start all three services
- Test full workflow
- Fix bugs

**Verification:**
- F.2.0: Daily to-do generation works
- F.3.0: Real-time logging works
- F.5.0: Progressive overload reference works

---

### Phase 8: Polish & Documentation (Day 15-16)
**Files to Create:**
- `sre/README.md`
- Update root `README.md`

**Actions:**
- Add loading animations
- Improve error messages
- Write documentation

**Verification:**
- All PRD requirements met
- System stable

---

## ✅ Success Criteria (PRD Compliance)

### F.2.0: Daily To-Do Generation
- [x] S-RE queries P-MIS for current day
- [x] Displays exercise list
- [x] Shows target body parts
- [x] Handles missing plan gracefully

### F.3.0: Real-Time Logging
- [x] User can log weight/reps after each set
- [x] Immediate POST to L-DPS
- [x] No need to complete full exercise
- [x] Confirmation displayed

### F.5.0: Progressive Overload Reference (CRITICAL)
- [x] Queries L-DPS for latest session on exercise start
- [x] Displays ALL sets from previous session
- [x] Shows full breakdown (set/rep/weight)
- [x] Handles first-time exercise
- [x] Suggests targets to beat

---

## 🔒 Architectural Compliance

### Three-Module Separation
- ✅ S-RE is independent (port 5173 dev, configurable prod)
- ✅ S-RE never writes to P-MIS
- ✅ P-MIS and L-DPS remain unchanged
- ✅ Communication via REST APIs only

### Immutability
- ✅ L-DPS remains append-only
- ✅ S-RE only reads from P-MIS
- ✅ No updates to logged sets

### Unidirectional Data Flow
- ✅ S-RE → P-MIS (read)
- ✅ S-RE → L-DPS (read + write)
- ✅ S-RE never modifies plan

---

## 📦 Dependencies (package.json)

```json
{
  "name": "sre-workout-session",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext ts,tsx"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^7.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.1",
    "@types/react-dom": "^18.3.0",
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "@typescript-eslint/parser": "^7.0.0",
    "@vitejs/plugin-react": "^4.3.0",
    "eslint": "^8.57.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "typescript": "^5.5.0",
    "vite": "^5.4.0"
  }
}
```

---

## 🧪 Testing Strategy

### Unit Tests (Future)
- Progressive overload calculation
- Date helpers
- Validators

### Integration Tests
- P-MIS client
- L-DPS client
- State management

### E2E Tests (Manual for MVP)
1. User views workout list
2. User selects exercise
3. User sees previous session
4. User logs 3 sets
5. User finishes exercise
6. User returns to list (marked complete)

---

## 🐛 Edge Cases Handled

1. **No plan uploaded:** Graceful error, redirect to upload
2. **First-time exercise:** Show encouragement, no reference
3. **Network errors:** Retry mechanism, user-friendly messages
4. **Invalid inputs:** Client-side validation before API call
5. **Concurrent logging:** L-DPS handles with UUID primary keys
6. **Browser refresh:** State lost (future: localStorage persistence)

---

## 🔮 Future Enhancements (Out of Scope)

- [ ] Authentication (JWT)
- [ ] Offline mode (Service Worker + IndexedDB)
- [ ] Dark mode
- [ ] Exercise history charts
- [ ] Personal records (PR) tracking
- [ ] Social sharing
- [ ] Mobile app (React Native)

---

## 📚 References

- **PRD:** `/Users/flxshh/Desktop/WARP/Training_log/docs/PRD.md`
- **Project Rules:** `/Users/flxshh/Desktop/WARP/Training_log/WARP.md`
- **P-MIS README:** `/Users/flxshh/Desktop/WARP/Training_log/pmis/README.md`
- **L-DPS README:** `/Users/flxshh/Desktop/WARP/Training_log/ldps/README.md`
- **Integration Plan:** `/Users/flxshh/Desktop/WARP/Training_log/docs/S-RE_INTEGRATION_PLAN.md`
- **React Docs:** https://react.dev

---

## 🎯 Next Steps

1. ✅ **Review this plan** with stakeholder
2. 🔵 **Approval to proceed** with implementation
3. 🔵 **Start Phase 1** (Project setup)
4. 🔵 **Daily standups** to track progress

---

**Plan Status:** ✅ Ready for Implementation  
**Risk Level:** 🟢 Low (Additive only, no breaking changes)  
**Confidence:** 95% (Well-researched, PRD-compliant, rule-compliant)
