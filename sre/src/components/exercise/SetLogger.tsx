/**
 * SetLogger Component
 * 
 * PRD F.3.0 - Real-Time Logging
 * Allows users to log weight, reps, and optional RPE after completing a set
 */

import { useState, FormEvent } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'

interface SetLoggerProps {
  setNumber: number
  onLogSet: (weight: number, reps: number, rpe?: number) => Promise<void>
  suggestedWeight?: number
  suggestedReps?: number
}

export function SetLogger({
  setNumber,
  onLogSet,
  suggestedWeight,
  suggestedReps,
}: SetLoggerProps) {
  const [weight, setWeight] = useState(suggestedWeight?.toString() || '')
  const [reps, setReps] = useState(suggestedReps?.toString() || '')
  const [rpe, setRpe] = useState('')
  const [isLogging, setIsLogging] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()

    const weightNum = parseFloat(weight)
    const repsNum = parseInt(reps, 10)
    const rpeNum = rpe ? parseInt(rpe, 10) : undefined

    // Validation
    if (isNaN(weightNum) || isNaN(repsNum)) {
      setError('Please enter valid numbers')
      return
    }

    if (weightNum <= 0 || repsNum <= 0) {
      setError('Weight and reps must be positive')
      return
    }

    if (rpeNum && (rpeNum < 1 || rpeNum > 10)) {
      setError('RPE must be between 1 and 10')
      return
    }

    setIsLogging(true)
    setError(null)

    try {
      await onLogSet(weightNum, repsNum, rpeNum)
      // Reset for next set
      setWeight('')
      setReps('')
      setRpe('')
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setIsLogging(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Log Set {setNumber}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="weight">Weight (kg)</Label>
              <Input
                id="weight"
                type="number"
                step="0.5"
                value={weight}
                onChange={(e) => setWeight(e.target.value)}
                placeholder="62.5"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="reps">Reps</Label>
              <Input
                id="reps"
                type="number"
                value={reps}
                onChange={(e) => setReps(e.target.value)}
                placeholder="10"
                min="1"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="rpe">RPE (Optional - Rate 1-10)</Label>
            <Input
              id="rpe"
              type="number"
              value={rpe}
              onChange={(e) => setRpe(e.target.value)}
              placeholder="7"
              min="1"
              max="10"
            />
          </div>

          {error && (
            <p className="text-sm text-destructive">{error}</p>
          )}

          <Button 
            type="submit" 
            className="w-full" 
            size="lg"
            disabled={isLogging}
          >
            {isLogging ? 'Logging...' : `Log Set ${setNumber}`}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
