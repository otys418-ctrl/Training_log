/**
 * ExerciseCard Component
 * 
 * Displays a single exercise from the daily workout plan
 * Shows exercise name, sets/reps info, and completion status
 */

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Exercise } from '@/api/types'

interface ExerciseCardProps {
  exercise: Exercise
  isCompleted?: boolean
  onStart: () => void
}

export function ExerciseCard({ exercise, isCompleted = false, onStart }: ExerciseCardProps) {
  return (
    <Card className={isCompleted ? 'border-primary' : ''}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">{exercise.name}</CardTitle>
          {isCompleted && (
            <Badge variant="secondary" className="ml-2">
              ✓ Done
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex gap-3 text-sm text-muted-foreground">
          {exercise.sets && <span>{exercise.sets} sets</span>}
          {exercise.reps && <span>× {exercise.reps} reps</span>}
        </div>
        <Button 
          onClick={onStart} 
          variant={isCompleted ? 'outline' : 'default'}
          className="w-full"
        >
          {isCompleted ? 'Review' : 'Start Exercise'}
        </Button>
      </CardContent>
    </Card>
  )
}
