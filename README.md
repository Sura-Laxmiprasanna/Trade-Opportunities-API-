\# Market Analysis API



\## Overview

This is a FastAPI application that provides market analysis reports for different sectors in \*\*markdown format\*\*.  

It integrates mock market data and a simulated AI (Gemini API) for analysis.



\---



\## Features

\- Single endpoint: `/analyze/{sector}`

\- Returns \*\*markdown market analysis report\*\*

\- \*\*API key authentication\*\* for security

\- \*\*Rate limiting\*\*: 5 requests per minute per client

\- Input validation for allowed sectors (`technology`, `finance`, `healthcare`, `energy`)

\- OpenAPI / Swagger documentation at `/docs`



\---



\## Requirements

\- Python 3.10+

\- FastAPI

\- Uvicorn



Install dependencies:



```bash

pip install fastapi uvicorn.

