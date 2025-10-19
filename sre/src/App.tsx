/**
 * S-RE App
 * 
 * Main application component with routing and state management
 * Integrates WorkoutProvider for global state across all pages
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { WorkoutProvider } from '@/context/WorkoutContext'
import { WorkoutListPage } from '@/pages/WorkoutListPage'
import { ExerciseDetailPage } from '@/pages/ExerciseDetailPage'

function App() {
  return (
    <WorkoutProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<WorkoutListPage />} />
          <Route path="/exercise/:exerciseName" element={<ExerciseDetailPage />} />
        </Routes>
      </BrowserRouter>
    </WorkoutProvider>
  )
}

export default App
