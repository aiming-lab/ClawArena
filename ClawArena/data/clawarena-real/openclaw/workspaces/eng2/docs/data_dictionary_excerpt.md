# TLC Yellow Taxi — Data Dictionary (excerpt, verbatim)

Source: NYC TLC Trip Record Data / Azure Open Datasets.

| Field | Meaning |
|---|---|
| `VendorID` | TPEP provider code (1, 2; 6 = sandbox) |
| `tpep_pickup_datetime` | Meter engaged datetime |
| `tpep_dropoff_datetime` | Meter disengaged datetime |
| `passenger_count` | Driver-entered passenger count (nullable) |
| `trip_distance` | Trip miles reported by the taximeter |
| `RatecodeID` | 1=Standard 2=JFK 3=Newark 4=Nassau/Westchester 5=Negotiated 6=Group ride |
| `PULocationID` / `DOLocationID` | TLC Taxi Zone (1–265) |
| `payment_type` | 1=Credit card 2=Cash 3=No charge 4=Dispute 5=Unknown 6=Voided |
| `fare_amount` | Meter fare (USD) |
| `congestion_surcharge` | NYS congestion surcharge (USD 2.50 for yellow taxi, since 2019) |
| `airport_fee` | LGA/JFK pickup fee (USD 1.25, since 2022) |
| `cbd_congestion_fee` | CBD congestion relief toll (USD 0.75, effective 2025-01-05) |

Use these exact field names in all pipeline code and reports.
