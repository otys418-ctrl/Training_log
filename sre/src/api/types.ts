/**
 * TypeScript type definitions for S-RE API layer
 * Mirrors P-MIS and L-DPS schemas for type safety
 */

// ============================================================================
// P-MIS Types (Plan Management & Ingestion Service)
// ============================================================================

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

export interface PlanResponse {
  plan_id: string;
  user_id: string;
  workouts: DailyWorkout[];
  created_at: string;
}

// ============================================================================
// L-DPS Types (Logbook & Data Persistence Service)
// ============================================================================

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

export interface ExerciseHistoryResponse {
  user_id: string;
  exercise_name: string;
  total_entries: number;
  entries: LogEntryResponse[];
}

// ============================================================================
// Error Types
// ============================================================================

export interface APIError {
  detail: string;
  status?: number;
}
