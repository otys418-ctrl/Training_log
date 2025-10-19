import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'

function App() {
  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold tracking-tight">S-RE: Workout Session Engine</h1>
          <p className="text-muted-foreground">Testing ShadCN + Tailwind Integration</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Component Test</CardTitle>
            <CardDescription>
              Verifying all ShadCN components are working correctly
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Buttons */}
            <div className="space-y-2">
              <Label>Button Variants</Label>
              <div className="flex flex-wrap gap-2">
                <Button>Default</Button>
                <Button variant="secondary">Secondary</Button>
                <Button variant="outline">Outline</Button>
                <Button variant="ghost">Ghost</Button>
                <Button variant="destructive">Destructive</Button>
              </div>
            </div>

            {/* Inputs */}
            <div className="space-y-2">
              <Label htmlFor="test-input">Input Field</Label>
              <Input 
                id="test-input" 
                type="text" 
                placeholder="Enter weight (kg)" 
              />
            </div>

            {/* Badges */}
            <div className="space-y-2">
              <Label>Badge Variants</Label>
              <div className="flex gap-2">
                <Badge>Default</Badge>
                <Badge variant="secondary">Secondary</Badge>
                <Badge variant="outline">Outline</Badge>
                <Badge variant="destructive">Destructive</Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Workout Simulation Card */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Bench Press</CardTitle>
              <Badge variant="secondary">3 sets</Badge>
            </div>
            <CardDescription>Last session: 60kg × 10 reps</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="weight">Weight (kg)</Label>
                <Input id="weight" type="number" placeholder="62.5" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="reps">Reps</Label>
                <Input id="reps" type="number" placeholder="10" />
              </div>
            </div>
            <Button className="w-full" size="lg">
              Log Set 1
            </Button>
          </CardContent>
        </Card>

        <div className="text-center text-sm text-muted-foreground">
          <p>✅ Tailwind CSS working</p>
          <p>✅ ShadCN components loaded</p>
          <p>✅ Design tokens applied</p>
        </div>
      </div>
    </div>
  )
}

export default App
