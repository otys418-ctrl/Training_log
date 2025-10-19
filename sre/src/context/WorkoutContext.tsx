/**
 * Workout Context
 * 
 * React Context + useReducer for global workout session state management
 * Follows official React documentation pattern for Context + Reducer
 * Reference: https://react.dev/learn/scaling-up-with-reducer-and-context
 */

import { createContext, useContext, useReducer, ReactNode, Dispatch } from 'react';
import { workoutReducer, createInitialState, WorkoutState, WorkoutAction } from './workoutReducer';

// ============================================================================
// Context Creation
// ============================================================================

const WorkoutContext = createContext<WorkoutState | undefined>(undefined);
const WorkoutDispatchContext = createContext<Dispatch<WorkoutAction> | undefined>(undefined);

// ============================================================================
// Provider Component
// ============================================================================

interface WorkoutProviderProps {
  children: ReactNode;
  userId?: string; // Allow custom userId for testing or auth
}

export function WorkoutProvider({ children, userId }: WorkoutProviderProps) {
  const [state, dispatch] = useReducer(workoutReducer, createInitialState(userId));

  return (
    <WorkoutContext.Provider value={state}>
      <WorkoutDispatchContext.Provider value={dispatch}>
        {children}
      </WorkoutDispatchContext.Provider>
    </WorkoutContext.Provider>
  );
}

// ============================================================================
// Custom Hooks
// ============================================================================

/**
 * Hook to access workout state
 * 
 * @returns Current workout state
 * @throws Error if used outside WorkoutProvider
 * 
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { dailyWorkout, isLoading } = useWorkout();
 *   return <div>{isLoading ? 'Loading...' : dailyWorkout?.day}</div>;
 * }
 * ```
 */
export function useWorkout(): WorkoutState {
  const context = useContext(WorkoutContext);
  if (context === undefined) {
    throw new Error('useWorkout must be used within a WorkoutProvider');
  }
  return context;
}

/**
 * Hook to access dispatch function for workout actions
 * 
 * @returns Dispatch function for workout actions
 * @throws Error if used outside WorkoutProvider
 * 
 * @example
 * ```tsx
 * function MyComponent() {
 *   const dispatch = useWorkoutDispatch();
 *   const handleClick = () => {
 *     dispatch({ type: 'LOAD_WORKOUT_START' });
 *   };
 *   return <button onClick={handleClick}>Load Workout</button>;
 * }
 * ```
 */
export function useWorkoutDispatch(): Dispatch<WorkoutAction> {
  const context = useContext(WorkoutDispatchContext);
  if (context === undefined) {
    throw new Error('useWorkoutDispatch must be used within a WorkoutProvider');
  }
  return context;
}

// ============================================================================
// Convenience Hook (Optional - combines both)
// ============================================================================

/**
 * Hook that returns both state and dispatch
 * Useful when you need both in the same component
 * 
 * @returns Tuple of [state, dispatch]
 * 
 * @example
 * ```tsx
 * function MyComponent() {
 *   const [state, dispatch] = useWorkoutContext();
 *   // Use both state and dispatch
 * }
 * ```
 */
export function useWorkoutContext(): [WorkoutState, Dispatch<WorkoutAction>] {
  return [useWorkout(), useWorkoutDispatch()];
}
