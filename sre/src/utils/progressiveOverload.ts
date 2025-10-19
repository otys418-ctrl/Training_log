/**
 * Progressive Overload Logic
 * 
 * Algorithms for calculating progression suggestions and tracking performance improvements
 * Core feature for PRD F.5.0 - Progressive Overload Reference
 */

import { SessionReference } from '../api/types';

// ============================================================================
// Types
// ============================================================================

export interface Progression {
  suggestedWeight: number;
  suggestedReps: number;
  lastWeight: number;
  lastReps: number;
  strategy: 'weight' | 'reps' | 'both';
  message: string;
}

// ============================================================================
// Progression Calculation
// ============================================================================

/**
 * Calculate progressive overload suggestions based on previous session
 * 
 * Strategy:
 * - If reps < 12: Add 1 rep (rep progression)
 * - If reps >= 12: Add 2.5kg, reduce reps to comfortable range (weight progression)
 * 
 * @param reference - Previous session reference data
 * @returns Progression suggestions
 */
export function calculateProgression(reference: SessionReference): Progression {
  // Find the heaviest set from last session
  const heaviestSet = reference.sets.reduce((max, set) =>
    set.weight_used > max.weight_used ? set : max
  );

  const lastWeight = heaviestSet.weight_used;
  const lastReps = heaviestSet.reps_completed;

  let suggestedWeight = lastWeight;
  let suggestedReps = lastReps;
  let strategy: 'weight' | 'reps' | 'both' = 'reps';

  if (lastReps < 12) {
    // Add reps first (easier progression)
    suggestedReps = lastReps + 1;
    strategy = 'reps';
  } else {
    // Add weight, reset reps to comfortable range
    suggestedWeight = lastWeight + 2.5;
    suggestedReps = Math.max(8, lastReps - 2);
    strategy = 'weight';
  }

  const message =
    strategy === 'reps'
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
 * 
 * Progressive overload is achieved if:
 * 1. More weight at same or more reps
 * 2. Same weight with more reps
 * 
 * @param currentWeight - Weight used in current set
 * @param currentReps - Reps completed in current set
 * @param reference - Previous session reference
 * @returns true if current set beats previous best
 */
export function isBeatPreviousSession(
  currentWeight: number,
  currentReps: number,
  reference: SessionReference
): boolean {
  const heaviestSet = reference.sets.reduce((max, set) =>
    set.weight_used > max.weight_used ? set : max
  );

  return (
    currentWeight > heaviestSet.weight_used ||
    (currentWeight === heaviestSet.weight_used && currentReps > heaviestSet.reps_completed)
  );
}

/**
 * Calculate total volume for a session
 * Volume = Sum of (weight × reps) for all sets
 * 
 * @param reference - Session reference data
 * @returns Total volume in kg
 */
export function calculateVolume(reference: SessionReference): number {
  return reference.sets.reduce((sum, set) => sum + set.weight_used * set.reps_completed, 0);
}

/**
 * Find the best set (highest weight) from a session
 * 
 * @param reference - Session reference data
 * @returns The set with highest weight
 */
export function findBestSet(reference: SessionReference) {
  return reference.sets.reduce((max, set) => (set.weight_used > max.weight_used ? set : max));
}

/**
 * Calculate percentage improvement over previous session
 * 
 * @param currentWeight - Current weight
 * @param currentReps - Current reps
 * @param reference - Previous session
 * @returns Percentage improvement (e.g., 5.2 for 5.2%)
 */
export function calculateImprovement(
  currentWeight: number,
  currentReps: number,
  reference: SessionReference
): number {
  const heaviestSet = findBestSet(reference);
  const previousBest = heaviestSet.weight_used * heaviestSet.reps_completed;
  const currentBest = currentWeight * currentReps;

  return ((currentBest - previousBest) / previousBest) * 100;
}
