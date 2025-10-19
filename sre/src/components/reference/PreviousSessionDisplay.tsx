/**
 * PreviousSessionDisplay Component
 * 
 * PRD F.5.0 - Progressive Overload Reference (CRITICAL)
 * Displays ALL sets from the most recent session of an exercise
 * Enables users to see exactly what they need to beat
 */

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { SessionReference } from '@/api/types'
import { calculateVolume, findBestSet } from '@/utils/progressiveOverload'

interface PreviousSessionDisplayProps {
  reference: SessionReference | null
  isLoading: boolean
}

export function PreviousSessionDisplay({ reference, isLoading }: PreviousSessionDisplayProps) {
  if (isLoading) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="text-center text-muted-foreground">
            Loading previous session...
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!reference) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="text-center space-y-2">
            <p className="text-lg">🎉 First time doing this exercise!</p>
            <p className="text-sm text-muted-foreground">Set your baseline performance</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  const totalVolume = calculateVolume(reference)
  const heaviestSet = findBestSet(reference)
  const sessionDate = new Date(reference.session_timestamp).toLocaleDateString()

  return (
    <Card>
      <CardHeader>
        <CardTitle>Last Session</CardTitle>
        <CardDescription>{sessionDate}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Summary Stats */}
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold">{reference.total_sets}</div>
            <div className="text-xs text-muted-foreground">Total Sets</div>
          </div>
          <div>
            <div className="text-2xl font-bold">{totalVolume.toFixed(0)}</div>
            <div className="text-xs text-muted-foreground">Volume (kg)</div>
          </div>
          <div>
            <div className="text-2xl font-bold">
              {heaviestSet.weight_used}kg
            </div>
            <div className="text-xs text-muted-foreground">Best Weight</div>
          </div>
        </div>

        {/* Set-by-Set Breakdown */}
        <div className="space-y-2">
          <div className="text-sm font-medium">Set Breakdown</div>
          {reference.sets.map((set, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between p-2 rounded-md bg-muted/50"
            >
              <span className="text-sm font-medium">Set {set.set_number}</span>
              <div className="flex items-center gap-2">
                <span className="text-sm">
                  {set.weight_used}kg × {set.reps_completed} reps
                </span>
                {set.rpe && (
                  <Badge variant="outline" className="text-xs">
                    RPE {set.rpe}
                  </Badge>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
