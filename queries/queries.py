temp_table = """
    CREATE OR REPLACE TEMP TABLE crashes AS
    SELECT 
        BOROUGH,
        "CRASH DATE",
        EXTRACT(YEAR FROM "CRASH DATE") AS YEAR, 
        COALESCE("NUMBER OF PERSONS KILLED",0) AS PERSONS_KILLED,
        COALESCE("NUMBER OF PERSONS INJURED",0) AS PERSONS_INJURED,
        "CONTRIBUTING FACTOR VEHICLE 1",
        "CONTRIBUTING FACTOR VEHICLE 2",
        "CONTRIBUTING FACTOR VEHICLE 3",
        "CONTRIBUTING FACTOR VEHICLE 4",
        "CONTRIBUTING FACTOR VEHICLE 5",
        "VEHICLE TYPE CODE 1",
        "VEHICLE TYPE CODE 2",
        "VEHICLE TYPE CODE 3",
        "VEHICLE TYPE CODE 4",
        "VEHICLE TYPE CODE 5" ,
        "ON STREET NAME",
        "NUMBER OF PERSONS INJURED",    
        "NUMBER OF PERSONS KILLED",
        LONGITUDE,
        LATITUDE 
    FROM geo_crashes.parquet
"""

kpi_query = """
    SELECT 
        COUNT(*) AS total_collisions, 
        SUM(PERSONS_KILLED) AS persons_killed, 
        SUM(PERSONS_INJURED) AS persons_injured
    FROM crashes
    WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ?
"""

word_query = """
WITH factors AS (
  SELECT UNNEST(ARRAY[
      "CONTRIBUTING FACTOR VEHICLE 1",
      "CONTRIBUTING FACTOR VEHICLE 2",
      "CONTRIBUTING FACTOR VEHICLE 3",
      "CONTRIBUTING FACTOR VEHICLE 4",
      "CONTRIBUTING FACTOR VEHICLE 5"
  ]) AS reasons
  FROM crashes
  WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ?
),
reasons AS (
  SELECT reasons, COUNT(reasons) AS Count
  FROM factors
  GROUP BY reasons
  ORDER BY Count DESC
  LIMIT 25
)
SELECT
    CASE reasons
        WHEN 'Driver Inattention/Distraction' THEN 'Distraction'
        WHEN 'Failure to Yield Right-of-Way' THEN 'Right-of-Way Violation'
        WHEN 'Following Too Closely' THEN 'Tailgating'
        WHEN 'Other Vehicular' THEN 'Other Vehicles'
        WHEN 'Backing Unsafely' THEN 'Unsafe Backing'
        WHEN 'Passing or Lane Usage Improper' THEN 'Improper Passing'
        WHEN 'Passing Too Closely' THEN 'Close Passing'
        WHEN 'Turning Improperly' THEN 'Improper Turn'
        WHEN 'Fatigued/Drowsy' THEN 'Fatigue'
        WHEN 'Unsafe Lane Changing' THEN 'Lane Change'
        WHEN 'Traffic Control Disregarded' THEN 'Traffic Violation'
        WHEN 'Driver Inexperience' THEN 'Inexperience'
        WHEN 'Unsafe Speed' THEN 'Speeding'
        WHEN 'Alcohol Involvement' THEN 'Alcohol'
        WHEN 'Lost Consciousness' THEN 'Unconscious'
        WHEN 'Pavement Slippery' THEN 'Slippery Road'
        WHEN 'Prescription Medication' THEN 'Medication'
        WHEN 'View Obstructed/Limited' THEN 'Obstructed View'
        WHEN 'Outside Car Distraction' THEN 'Distraction'
        WHEN 'Oversized Vehicle' THEN 'Oversized Vehicle'
        WHEN 'Pedestrian/Bicyclist/Other Pedestrian Error/Confusion' THEN 'Pedestrian Error'
        WHEN 'Aggressive Driving/Road Rage' THEN 'Road Rage'
        WHEN 'Physical Disability' THEN 'Disability'
        ELSE 'Other/Unknown'
    END AS Word,
    Count
FROM reasons;
"""

bar_query = """
WITH all_vehicles AS (
    SELECT 
        BOROUGH,
        YEAR,
        UNNEST([
            "VEHICLE TYPE CODE 1",
            "VEHICLE TYPE CODE 2",
            "VEHICLE TYPE CODE 3",
            "VEHICLE TYPE CODE 4",
            "VEHICLE TYPE CODE 5"
        ]) AS vehicle_type
    FROM crashes
    WHERE BOROUGH IN ? 
      AND YEAR BETWEEN ? AND ?
)
SELECT 
    CASE 
        WHEN UPPER(vehicle_type) = 'STATION WAGON/SPORT UTILITY VEHICLE' THEN 'SUV'
        WHEN UPPER(vehicle_type) = 'SPORT UTILITY / STATION WAGON' THEN 'SPORT'
        ELSE UPPER(vehicle_type)
    END AS Vehicle,
    COUNT(*) AS counts
FROM all_vehicles
WHERE vehicle_type IS NOT NULL AND vehicle_type <> ''
GROUP BY Vehicle
ORDER BY counts DESC
LIMIT 6;
"""

pie_query = """SELECT
  (
    CASE WHEN "VEHICLE TYPE CODE 1" IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN "VEHICLE TYPE CODE 2" IS NOT NULL THEN 1 ELSE 0 END +
    CASE WHEN "VEHICLE TYPE CODE 3" IS NOT NULL THEN 1 ELSE 0 END 
  ) AS vehicle_count,
  COUNT(*) AS crashes
FROM crashes
WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ?
GROUP BY vehicle_count
ORDER BY vehicle_count
"""


line_query = """
SELECT 
    BOROUGH,
    YEAR AS Year,
    COUNT(*) AS total_collisions
FROM crashes
WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ?
GROUP BY BOROUGH,YEAR
ORDER BY BOROUGH, YEAR;
"""

table_query = """SELECT 
      STRFTIME("CRASH DATE", '%b/%d/%Y') AS DATE,
      BOROUGH,
      "ON STREET NAME",
      "NUMBER OF PERSONS INJURED",
      "NUMBER OF PERSONS KILLED",
      "CONTRIBUTING FACTOR VEHICLE 1" AS "CONTRIBUTING FACTOR",
      "VEHICLE TYPE CODE 1" AS "VEHICLE TYPE"
FROM crashes
WHERE BOROUGH IN ? AND "CRASH DATE" = (SELECT MAX("CRASH DATE") FROM crashes)
ORDER BY "CRASH DATE" DESC
LIMIT 10;"""


map_query = """
SELECT
    BOROUGH,
    "ON STREET NAME",
    "NUMBER OF PERSONS INJURED",
    "NUMBER OF PERSONS KILLED",
    "CONTRIBUTING FACTOR VEHICLE 1",
    "VEHICLE TYPE CODE 1",
    LATITUDE, 
    LONGITUDE
FROM crashes
WHERE BOROUGH IN ? AND YEAR BETWEEN ? AND ? 
LIMIT 5000;"""
