/**
 * P-MIS API Client
 * 
 * Handles communication with Plan Management & Ingestion Service (port 8000)
 * PRD Reference: F.2.0 - Daily To-Do Generation
 */

import { DailyWorkout, PlanResponse, APIError } from './types';

const PMIS_BASE_URL = import.meta.env.VITE_PMIS_URL || 'http://localhost:8000';

export class PMISClient {
  private baseUrl: string;

  constructor(baseUrl = PMIS_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Fetch daily workout for a specific user and day (PRD F.2.0)
   * 
   * @param userId - User identifier
   * @param day - Day of week (e.g., "Monday", "Tuesday")
   * @returns DailyWorkout or null if not found
   * @throws Error on network or server errors
   */
  async getDailyWorkout(userId: string, day: string): Promise<DailyWorkout | null> {
    try {
      const response = await fetch(
        `${this.baseUrl}/api/v1/plans/${userId}/${encodeURIComponent(day)}`,
        { method: 'GET' }
      );

      if (response.status === 404) {
        return null; // No plan found for this day
      }

      if (!response.ok) {
        const error: APIError = await response.json().catch(() => ({
          detail: `P-MIS error: ${response.statusText}`,
          status: response.status,
        }));
        throw new Error(error.detail);
      }

      return response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Failed to fetch daily workout');
    }
  }

  /**
   * Fetch complete training plan for a user
   * 
   * @param userId - User identifier
   * @returns Complete PlanResponse
   * @throws Error on network or server errors
   */
  async getFullPlan(userId: string): Promise<PlanResponse | null> {
    try {
      const response = await fetch(
        `${this.baseUrl}/api/v1/plans/${userId}`,
        { method: 'GET' }
      );

      if (response.status === 404) {
        return null;
      }

      if (!response.ok) {
        const error: APIError = await response.json().catch(() => ({
          detail: `P-MIS error: ${response.statusText}`,
          status: response.status,
        }));
        throw new Error(error.detail);
      }

      return response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Failed to fetch training plan');
    }
  }

  /**
   * Health check for P-MIS service
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
export const pmisClient = new PMISClient();
