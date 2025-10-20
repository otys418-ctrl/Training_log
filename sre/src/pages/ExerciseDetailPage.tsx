/**
 * ExerciseDetailPage
 * 
 * PRD F.3.0 - Real-Time Logging
 * PRD F.5.0 - Progressive Overload Reference (CRITICAL)
 * 
 * Main workout screen where users:
 * 1. See previous session performance (from L-DPS)
 * 2. Get progressive overload suggestions
 * 3. Log sets in real-time (to L-DPS)
 */

import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useWorkout, useWorkoutDispatch } from '@/context/WorkoutContext'
import { ldpsClient } from '@/api/ldps.client'
import { PreviousSessionDisplay } from '@/components/reference/PreviousSessionDisplay'
import { SetLogger } from '@/components/exercise/SetLogger'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { calculateProgression } from '@/utils/progressiveOverload'

export function ExerciseDetailPage() {
  const { exerciseName } = useParams<{ exerciseName: string }>()
  const state = useWorkout()
  const dispatch = useWorkoutDispatch()
  const navigate = useNavigate()
  const [isLoadingReference, setIsLoadingReference] = useState(false)

  const decodedName = decodeURIComponent(exerciseName || '')

  useEffect(() => {
    if (decodedName) {
      loadReference()
    }
  }, [decodedName])

  const loadReference = async () => {
    setIsLoadingReference(true)
    try {
      const reference = await ldpsClient.getLatestSession(state.userId, decodedName)
      dispatch({ type: 'LOAD_REFERENCE_SUCCESS', payload: reference })
    } catch (err) {
      console.error('Failed to load reference:', err)
      dispatch({ type: 'LOAD_REFERENCE_SUCCESS', payload: null })
    } finally {
      setIsLoadingReference(false)
    }
  }

  const handleLogSet = async (weight: number, reps: number, rpe?: number) => {
    const setNumber = state.loggedSets.length + 1

    const logEntry = {
      user_id: state.userId,
      exercise_name: decodedName,
      set_number: setNumber,
      weight_used: weight,
      reps_completed: reps,
      rpe,
    }

    const response = await ldpsClient.logSet(logEntry)
    dispatch({ type: 'LOG_SET_SUCCESS', payload: response })
  }

  const handleFinish = () => {
    // Mark exercise as completed if sets were logged
    if (state.loggedSets.length > 0) {
      dispatch({ type: 'COMPLETE_EXERCISE', payload: decodedName })
    }
    dispatch({ type: 'RESET_SESSION' })
    navigate('/')
  }

  const currentSetNumber = state.loggedSets.length + 1
  const progression = state.referenceData ? calculateProgression(state.referenceData) : null

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <Button variant="ghost" onClick={() => navigate('/')}>
              ← Back to Workout
            </Button>
            <h1 className="text-3xl font-bold mt-2">{decodedName}</h1>
          </div>
        </div>

        {/* Previous Session Reference */}
        <PreviousSessionDisplay
          reference={state.referenceData}
          isLoading={isLoadingReference}
        />

        {/* Progressive Overload Suggestion */}
        {progression && (
          <Card>
            <CardHeader>
              <CardTitle>Progressive Overload Target</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <span className="text-lg">
                  💪 Try <strong>{progression.suggestedWeight}kg</strong> × <strong>{progression.suggestedReps} reps</strong>
                </span>
                <Badge>{progression.strategy}</Badge>
              </div>
              <p className="text-sm text-muted-foreground mt-2">
                {progression.message}
              </p>
            </CardContent>
          </Card>
        )}

        {/* Current Session - Logged Sets */}
        {state.loggedSets.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Current Session</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {state.loggedSets.map((log) => (
                <div
                  key={log.log_entry_id}
                  className="flex items-center justify-between p-3 rounded-md bg-primary/10"
                >
                  <span className="font-medium">✅ Set {log.set_number}</span>
                  <span>
                    {log.weight_used}kg × {log.reps_completed} reps
                    {log.rpe && ` (RPE ${log.rpe})`}
                  </span>
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        {/* Set Logger */}
        <SetLogger
          setNumber={currentSetNumber}
          onLogSet={handleLogSet}
          suggestedWeight={progression?.suggestedWeight}
          suggestedReps={progression?.suggestedReps}
        />

        {/* Finish Button */}
        <Button
          variant="outline"
          onClick={handleFinish}
          className="w-full"
          size="lg"
        >
          Finish Exercise
        </Button>
      </div>
    </div>
  )
}
