"""
Plan Extractor using NLP and RegEx to extract structured training data
"""

import re
from typing import List, Dict, Any, Optional
import spacy


class PlanExtractor:
    """
    Extracts structured training plan data from raw text using NLP and pattern matching
    """
    
    # Common body parts for training
    BODY_PARTS = [
        "chest", "back", "shoulders", "legs", "arms", "biceps", "triceps",
        "quads", "hamstrings", "glutes", "calves", "abs", "core", "forearms"
    ]
    
    # Days of the week and other patterns
    DAYS = {
        "monday": "Monday", "mon": "Monday",
        "tuesday": "Tuesday", "tues": "Tuesday",
        "wednesday": "Wednesday", "wed": "Wednesday",
        "thursday": "Thursday", "thurs": "Thursday",
        "friday": "Friday", "fri": "Friday",
        "saturday": "Saturday", "sat": "Saturday",
        "sunday": "Sunday", "sun": "Sunday",
    }
    DAY_PATTERN = re.compile(r"(day|workout|session)[-:\s]*(\d+)", re.IGNORECASE)
    
    def __init__(self):
        """Initialize the extractor with spaCy model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Model not found - will need to be downloaded
            raise RuntimeError(
                "spaCy model 'en_core_web_sm' not found. "
                "Please install it using: python -m spacy download en_core_web_sm"
            )
    
    def extract(self, text: str, user_id: str) -> Dict[str, Any]:
        """
        Extract structured plan data from text
        
        Args:
            text: Raw text extracted from PDF
            user_id: User identifier
        
        Returns:
            Dictionary containing structured plan data
        """
        # Split text into sections by day
        daily_workouts = self._split_by_days(text)
        
        # Process each day
        plan_data = {
            "user_id": user_id,
            "workouts": []
        }
        
        for day, content in daily_workouts.items():
            workout = self._extract_daily_workout(day, content)
            if workout:
                plan_data["workouts"].append(workout)
        
        return plan_data
    
    def _split_by_days(self, text: str) -> Dict[str, str]:
        """
        Split text into sections by day of the week
        
        Args:
            text: Full text content
        
        Returns:
            Dictionary mapping day names to their content
        """
        daily_sections = {}
        lines = text.split('\n')
        current_day = None
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            found_day = None

            # Check for name patterns first (e.g., Monday)
            for day_key, day_name in self.DAYS.items():
                if day_key in line_lower.split():
                    found_day = day_name
                    break
            
            # If no name, check for numbered patterns (e.g., Day 1)
            if not found_day:
                match = self.DAY_PATTERN.search(line_lower)
                if match:
                    found_day = f"Day {match.group(2)}"
            
            if found_day:
                # Save previous day's content
                if current_day and current_content:
                    daily_sections[current_day] = '\n'.join(current_content)
                
                # Start new day
                current_day = found_day
                current_content = []
            elif current_day:
                current_content.append(line)
        
        # Save last day
        if current_day and current_content:
            daily_sections[current_day] = '\n'.join(current_content)
        
        return daily_sections
    
    def _extract_daily_workout(self, day: str, content: str) -> Optional[Dict[str, Any]]:
        """
        Extract workout details for a single day
        
        Args:
            day: Day of the week
            content: Text content for that day
        
        Returns:
            Dictionary containing workout details
        """
        # Extract target body parts
        target_body_parts = self._extract_body_parts(content)
        
        # Extract exercises
        exercises = self._extract_exercises(content)
        
        if not exercises:
            return None
        
        return {
            "day": day,
            "target_body_parts": target_body_parts,
            "exercises": exercises
        }
    
    def _extract_body_parts(self, content: str) -> List[str]:
        """
        Extract target body parts from content
        
        Args:
            content: Text content
        
        Returns:
            List of body part names
        """
        content_lower = content.lower()
        found_parts = []
        
        for part in self.BODY_PARTS:
            if part in content_lower:
                found_parts.append(part.capitalize())
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(found_parts))
    
    def _extract_exercises(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract exercise information including sets and reps
        
        Args:
            content: Text content
        
        Returns:
            List of exercise dictionaries
        """
        exercises = []
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            i += 1
            
            if not line:
                continue
            
            # Skip lines that look like data lines (not exercise names)
            if re.search(r'^(Set|Sets|Reps?|Duration|Weight)[:\s\d]', line, re.IGNORECASE):
                continue
            
            # This line is a potential exercise name
            exercise_name = line
            sets, reps = None, None
            
            # Look at the next line for set/rep data
            if i < len(lines):
                next_line = lines[i].strip()
                
                # Try to extract sets and reps from the next line
                # Pattern 1: "Sets 1–4" or "Set 1"
                sets_match = re.search(r'Sets?\s+\d+[–-]?(\d+)', next_line, re.IGNORECASE)
                if sets_match:
                    sets = int(sets_match.group(1))
                elif re.search(r'Set\s+\d+', next_line, re.IGNORECASE):
                    sets = 1  # Single set
                
                # Pattern 2: "Reps: 10" or "Reps: 10 each"
                reps_match = re.search(r'Reps?[:\s]+(\d+)', next_line, re.IGNORECASE)
                if reps_match:
                    reps = int(reps_match.group(1))
                
                # If we found data on the next line, consume it
                if sets is not None or reps is not None:
                    i += 1  # Skip the data line
            
            # Try single-line format as fallback (e.g., "Bench Press 3x10")
            if sets is None and reps is None:
                single_line_match = re.search(r'(\d+)\s*[x×]\s*(\d+)', line, re.IGNORECASE)
                if single_line_match:
                    sets = int(single_line_match.group(1))
                    reps = int(single_line_match.group(2))
                    exercise_name = line[:single_line_match.start()].strip()
            
            # Clean up exercise name
            # Remove body part in parentheses (e.g., "(Chest)")
            exercise_name = re.sub(r'\s*\([^)]+\)\s*$', '', exercise_name)
            # Remove common prefixes
            exercise_name = re.sub(r'^[-•*\d.)\s]+', '', exercise_name).strip()
            
            # Add to list if valid (must have actual text)
            if len(exercise_name) > 2 and re.search(r'[a-zA-Z]{2,}', exercise_name):
                exercises.append({
                    "name": exercise_name,
                    "sets": sets,
                    "reps": reps
                })
        
        return exercises
