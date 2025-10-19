/**
 * L-DPS API Client
 * 
 * Handles communication with Logbook & Data Persistence Service (port 8001)
 * PRD References: F.3.0 (Real-Time Logging), F.5.0 (Progressive Overload Reference - CRITICAL)
 */

import { LogEntryCreate, LogEntryResponse, SessionReference, APIError } from './types';

const LDPS_BASE_URL = import.meta.env.VITE_LDPS_URL || 'http://localhost:8001';

export class LDPSClient {
  private baseUrl: string;

  constructor(baseUrl = LDPS_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Get latest session reference for an exercise (PRD F.5.0 - CRITICAL)
   * 
   * Returns ALL sets from the single most recent session of this exercise.
   * This is the core feature enabling Progressive Overload tracking.
   * 
   * @param userId - User identifier
   * @param exerciseName - Exercise name (will be URL-encoded)
   * @param sessionThresholdHours - Hours between sets indicating new session (default: 2.0)
   * @returns SessionReference with all sets from latest session, or null if first time
   * @throws Error on network or server errors
   */
  async getLatestSession(
    userId: string,
    exerciseName: string,
    sessionThresholdHours = 2.0
  ): Promise<SessionReference | null> {
    try {
      const encodedName = encodeURIComponent(exerciseName);
      const url = `${this.baseUrl}/api/v1/logs/${userId}/${encodedName}/latest-session?session_threshold_hours=${sessionThresholdHours}`;

      const response = await fetch(url, { method: 'GET' });

      if (response.status === 404) {
        return null; // First time doing this exercise
      }

      if (!response.ok) {
        const error: APIError = await response.json().catch(() => ({
          detail: `L-DPS error: ${response.statusText}`,
          status: response.status,
        }));
        throw new Error(error.detail);
      }

      return response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Failed to fetch latest session');
    }
  }

  /**
   * Log a completed set (PRD F.3.0)
   * 
   * Creates an immutable log entry in L-DPS. Once logged, data cannot be modified.
   * 
   * @param logEntry - Log entry data with weight, reps, optional RPE
   * @returns Created log entry with auto-generated timestamp and ID
   * @throws Error on validation or network errors
   */
  async logSet(logEntry: LogEntryCreate): Promise<LogEntryResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/logs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(logEntry),
      });

      if (!response.ok) {
        const error: APIError = await response.json().catch(() => ({
          detail: `Failed to log set: ${response.statusText}`,
          status: response.status,
        }));
        throw new Error(error.detail);
      }

      return response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Failed to log set');
    }
  }

  /**
   * Get exercise history for a user (optional analytics)
   * 
   * @param userId - User identifier
   * @param exerciseName - Optional filter by exercise name
   * @param limit - Maximum entries to return (default: 100, max: 1000)
   * @returns Exercise history response
   * @throws Error on network or server errors
   */
  async getHistory(
    userId: string,
    exerciseName?: string,
    limit = 100
  ): Promise<LogEntryResponse[]> {
    try {
      let url = `${this.baseUrl}/api/v1/logs/${userId}/history?limit=${limit}`;
      if (exerciseName) {
        url += `&exercise_name=${encodeURIComponent(exerciseName)}`;
      }

      const response = await fetch(url, { method: 'GET' });

      if (!response.ok) {
        const error: APIError = await response.json().catch(() => ({
          detail: `L-DPS error: ${response.statusText}`,
          status: response.status,
        }));
        throw new Error(error.detail);
      }

      const data = await response.json();
      return data.entries || [];
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Failed to fetch exercise history');
    }
  }

  /**
   * Health check for L-DPS service
   * 
   * @returns true if service is operational
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/`);
      return response.ok;
    } catch {
      return false;
    }
  }
}

// Singleton instance for application-wide use
export const ldpsClient = new LDPSClient();
