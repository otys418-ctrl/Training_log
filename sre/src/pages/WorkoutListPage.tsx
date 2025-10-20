/**
 * WorkoutListPage
 * 
 * PRD F.2.0 - Daily To-Do Generation
 * Fetches and displays the user's scheduled workout for the current day from P-MIS
 */

import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useWorkout, useWorkoutDispatch } from '@/context/WorkoutContext'
import { pmisClient } from '@/api/pmis.client'
import { ExerciseCard } from '@/components/exercise/ExerciseCard'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'

export function WorkoutListPage() {
  const state = useWorkout()
  const dispatch = useWorkoutDispatch()
  const navigate = useNavigate()

  useEffect(() => {
    loadWorkout()
  }, [state.currentDay])

  const loadWorkout = async () => {
    dispatch({ type: 'LOAD_WORKOUT_START' })

    try {
      const workout = await pmisClient.getDailyWorkout(state.userId, state.currentDay)

      if (!workout) {
        dispatch({
          type: 'LOAD_WORKOUT_ERROR',
          payload: 'No workout plan found. Please upload a plan first.',
        })
        return
      }

      dispatch({ type: 'LOAD_WORKOUT_SUCCESS', payload: workout })
    } catch (err) {
      dispatch({
        type: 'LOAD_WORKOUT_ERROR',
        payload: (err as Error).message,
      })
    }
  }

  const handleStartExercise = (exerciseName: string, index: number) => {
    dispatch({
      type: 'SELECT_EXERCISE',
      payload: { exerciseName, index },
    })
    navigate(`/exercise/${encodeURIComponent(exerciseName)}`)
  }

  if (state.isLoading) {
    return (
      <div className="min-h-screen bg-background p-4 md:p-8">
        <div className="max-w-4xl mx-auto">
          <Card>
            <CardContent className="pt-6">
              <div className="text-center text-muted-foreground">
                Loading workout...
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  if (state.error) {
    return (
      <div className="min-h-screen bg-background p-4 md:p-8">
        <div className="max-w-4xl mx-auto">
          <Card>
            <CardContent className="pt-6 space-y-4">
              <p className="text-center text-destructive">{state.error}</p>
              <Button onClick={loadWorkout} className="w-full">
                Retry
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  if (!state.dailyWorkout) {
    return (
      <div className="min-h-screen bg-background p-4 md:p-8">
        <div className="max-w-4xl mx-auto">
          <Card>
            <CardContent className="pt-6">
              <p className="text-center text-muted-foreground">
                No workout scheduled for today
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="space-y-2">
          <h1 className="text-3xl font-bold">{state.currentDay}</h1>
          <p className="text-muted-foreground">
            {state.dailyWorkout.target_body_parts.join(', ')}
          </p>
        </div>

        {/* Exercise List */}
        <div className="grid gap-4 md:grid-cols-2">
          {state.dailyWorkout.exercises.map((exercise, idx) => (
            <ExerciseCard
              key={idx}
              exercise={exercise}
              isCompleted={state.completedExercises.has(exercise.name)}
              onStart={() => handleStartExercise(exercise.name, idx)}
            />
          ))}
        </div>

        {/* Progress */}
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-sm text-muted-foreground">
                {state.completedExercises.size} / {state.dailyWorkout.exercises.length} exercises completed
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
