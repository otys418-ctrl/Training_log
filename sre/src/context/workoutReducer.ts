/**
 * Workout Reducer
 * 
 * State management logic for workout session using React useReducer pattern
 * Follows official React documentation best practices
 */

import type { DailyWorkout, SessionReference, LogEntryResponse } from '../api/types';

// ============================================================================
// State Shape
// ============================================================================

export interface WorkoutState {
  userId: string;
  currentDay: string;
  dailyWorkout: DailyWorkout | null;
  currentExerciseIndex: number;
  currentExercise: string | null;
  referenceData: SessionReference | null;
  loggedSets: LogEntryResponse[];
  completedExercises: Set<string>; // Track completed exercise names
  isLoading: boolean;
  error: string | null;
}

// ============================================================================
// Action Types
// ============================================================================

export type WorkoutAction =
  | { type: 'SET_USER_ID'; payload: string }
  | { type: 'SET_CURRENT_DAY'; payload: string }
  | { type: 'LOAD_WORKOUT_START' }
  | { type: 'LOAD_WORKOUT_SUCCESS'; payload: DailyWorkout }
  | { type: 'LOAD_WORKOUT_ERROR'; payload: string }
  | { type: 'SELECT_EXERCISE'; payload: { exerciseName: string; index: number } }
  | { type: 'LOAD_REFERENCE_SUCCESS'; payload: SessionReference | null }
  | { type: 'LOG_SET_SUCCESS'; payload: LogEntryResponse }
  | { type: 'COMPLETE_EXERCISE'; payload: string } // Mark exercise as completed
  | { type: 'CLEAR_LOGGED_SETS' }
  | { type: 'RESET_SESSION' };

// ============================================================================
// Reducer Function
// ============================================================================

export function workoutReducer(state: WorkoutState, action: WorkoutAction): WorkoutState {
  switch (action.type) {
    case 'SET_USER_ID':
      return {
        ...state,
        userId: action.payload,
      };

    case 'SET_CURRENT_DAY':
      return {
        ...state,
        currentDay: action.payload,
      };

    case 'LOAD_WORKOUT_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };

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

    case 'COMPLETE_EXERCISE':
      return {
        ...state,
        completedExercises: new Set([...state.completedExercises, action.payload]),
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
      // Type-safe exhaustiveness check
      const _exhaustive: never = action;
      throw new Error(`Unknown action type: ${(_exhaustive as any).type}`);
  }
}

// ============================================================================
// Initial State Helper
// ============================================================================

export function getCurrentDay(): string {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  return days[new Date().getDay()];
}

/**
 * Map weekday names to Day numbers for plan lookup
 * Monday (Day-1) = "Day 1", Tuesday (Day-2) = "Day 2", etc.
 */
export function mapWeekdayToPlanDay(weekday: string): string {
  const dayMapping: Record<string, string> = {
    'Monday': 'Day 1',
    'Tuesday': 'Day 2', 
    'Wednesday': 'Day 3',
    'Thursday': 'Day 4',
    'Friday': 'Day 5',
    'Saturday': 'Day 6',
    'Sunday': 'Day 7'
  };
  
  return dayMapping[weekday] || weekday;
}

export function createInitialState(userId = 'userid20OCt_3'): WorkoutState {
  const todayWeekday = getCurrentDay();
  const planDay = mapWeekdayToPlanDay(todayWeekday);
  
  return {
    userId,
    currentDay: planDay, // Use mapped plan day (e.g., "Day 1" for Monday)
    dailyWorkout: null,
    currentExerciseIndex: -1,
    currentExercise: null,
    referenceData: null,
    loggedSets: [],
    completedExercises: new Set<string>(),
    isLoading: false,
    error: null,
  };
}
