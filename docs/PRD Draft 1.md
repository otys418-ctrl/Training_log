\*\*\* \*\* \* \*\* \*\*\*

\#\# 🏋️ Product Requirements Document (PRD) Outline: Progressive Overload Log

\#\#\# I. Introduction and Goals

| Field | Description |  
| :--- | :--- |  
| \*\*Product Name\*\* | Progressive Overload Log (P.O. Log) |  
| \*\*Primary Goal\*\* | To facilitate the Progressive Overload training principle by providing immediate, session-level feedback from the user's historical performance. |  
| \*\*Success Metric\*\* | Retention Rate: % of users who log 3+ workouts per week after the first month. Core Usage: Average number of reference lookups per workout session. |

\*\*\* \*\* \* \*\* \*\*\*

\#\#\# II. Target Audience

| Segment | Description | |  
| :--- | :--- | :--- |  
| \*\*Primary Users\*\* | Dedicated Gym-Goers with a specified, structured training plan1. | |  
| \*\*User Pain Point\*\* | Losing track of specific weight/rep/set performance for a given exercise across different weeks, which prevents consistent progressive overload2. | |

\*\*\* \*\* \* \*\* \*\*\*

\#\#\# III. Modular System Architecture (Independent Components)

The application will be built on three core, independent services to ensure maximum scalability and separation of concerns.

\#\#\#\# 1\. Plan Management \\\\& Ingestion Service (P-MIS)

\* \*\*Purpose:\*\* To manage all scheduled training plans, including the initial ingestion of user-defined plans (e.g., from a PDF)3.  
\* \*\*Independence:\*\* This service is concerned only with what the user is scheduled to do. It is independent of how the user logs the data (Module 2).  
\* \*\*Data Model (Plan Schema):\*\*  
    \* Plan ID, User ID  
    \* Day (Monday, Tuesday, etc.)  
    \* Target Body Parts (e.g., Back, Biceps, Chest) 4  
    \* List of Planned Exercises (Name, Expected Sets/Reps/RPE, if provided).

\#\#\#\# 2\. Logbook \\\\& Data Persistence Service (L-DPS)

\* \*\*Purpose:\*\* The central, immutable ledger for all performance data. It is the single source of truth for all logged historical performance.  
\* \*\*Independence:\*\* This service only stores data. It doesn't know about the weekly plan (Module 1\) or how the data is displayed (Module 3).  
\* \*\*Data Model (Log Entry Schema):\*\*  
    \* Log Entry ID, User ID, Exercise Name  
    \* Timestamp (Date \\\\& Time)  
    \* Set Number  
    \* Weight Used (kg/lbs) 5  
    \* Reps Completed 6  
    \* Duration/Distance/RPE (Other measurable insights) 7

\#\#\#\# 3\. Workout Session \\\\& Reference Engine (S-RE)

\* \*\*Purpose:\*\* To orchestrate the real-time workout experience. It pulls data from the other two services to present the daily session and the historical reference information.  
\* \*\*Independence:\*\* This service is the UI/UX layer. It handles flow and display logic, but does not own any permanent data.  
\* \*\*Key Logic:\*\*  
    \* To-Do Generation: Based on the current day, query the P-MIS for the scheduled workout8.  
    \* Reference Retrieval: For a currently running exercise, query the L-DPS for the most recent log entries for that specific Exercise Name9.

\*\*\* \*\* \* \*\* \*\*\*

\#\#\# IV. Functional Requirements

| ID | Module | Feature Description | Acceptance Criteria |  
| :--- | :--- | :--- | :--- |  
| \*\*F.1.0\*\* | P-MIS | Plan Ingestion (PDF): Allow users to upload or paste a 7-day training plan10. | The system must successfully parse and store a minimum of 7 daily workouts with target body parts and exercise lists. |  
| \*\*F.2.0\*\* | S-RE, P-MIS | Daily To-Do Generation: Automatically populate the workout screen with the exercises scheduled for the current day11. | The application displays a list of exercises matching the current day's plan from the P-MIS. |  
| \*\*F.3.0\*\* | S-RE, L-DPS | Real-Time Logging: Provide an interface to log reps, weights, and set number after each set of an exercise12. | User can submit a log entry for a set without completing the full exercise session. This triggers an immediate call to L-DPS for storage. |  
| \*\*F.4.0\*\* | L-DPS | Data Persistence: Store all user-inputted measurable insights for every set13. | Logged data (Weight, Reps, Set \#) must be timestamped and permanently retrievable via User ID and Exercise Name. |  
| \*\*F.5.0\*\* | S-RE, L-DPS | Progressive Overload Reference: When the user begins an exercise, display the complete historical log data from the single most recent session that exact exercise was performed. | On the exercise logging screen, all logged sets (Sets 1-5, for example) from the previous workout must be displayed together as a reference, clearly showing the full set/rep/weight breakdown the user must aim to beat. |

\*\*\* \*\* \* \*\* \*\*\*

\#\#\# V. User Flow: Logging a Set

1\.  \*\*Start Session (S-RE):\*\* The user opens the app and starts their scheduled workout (e.g., "Leg Day").  
2\.  \*\*Select Exercise (S-RE):\*\* The user taps "Leg Press."  
3\.  \*\*Reference Data (S-RE \-\\\> L-DPS):\*\* S-RE queries L-DPS for the complete historical log data associated with the single most recent session of the current Exercise Name. L-DPS returns the full session's worth of set data. S-RE then displays this combined log (e.g., "Last Session: Set 1: 100kg x 10, Set 2: 105kg x 8, Set 3: 100kg x 10").  
4\.  \*\*Perform Set 1.\*\*  
5\.  \*\*Log Set 1 (S-RE \-\\\> L-DPS):\*\* The user inputs 110 kg and 8 reps for Set 1\. S-RE sends this log entry to L-DPS for persistent storage (F.4.0).  
6\.  \*\*Progressive Update (S-RE):\*\* The screen updates to show "Set 1 Logged: 110kg x 8."  
7\.  \*\*Perform Set 2.\*\*  
8\.  \*\*Log Set 2 (S-RE \-\\\> L-DPS):\*\* The user inputs 110 kg and 10 reps for Set 2\. L-DPS stores the new log entry.

\*\*\* \*\* \* \*\* \*\*\*  
