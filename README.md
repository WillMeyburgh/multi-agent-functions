# Objective

To create an AI to solve complex interrelated tasks via the use of multiple specialized agents to collaborate on solving multi-step tasks.

- Have the agents stored in a database
- Have a user-facing agent that creates an action plan with specified agents to fulfill user requests
- Google Tasks Agent and Google Calendar Agent
- Perform multi-step functions, such as getting all tasklist IDs then adding a task to a specified tasklist

## Prerequisites

### Google API Credentials (`credentials.json`)

This project requires a `credentials.json` file in the root directory to authenticate with Google APIs. The credentials must have access enabled for the Google Tasks API and Google Calendar API.

Refer to the Google Cloud documentation for instructions on how to obtain these credentials.

### Environment Variables (`.env`)

The project uses environment variables for configuration. Create a `.env` file in the root directory and define the following variables:

- `GOOGLE_API_KEY`: Your Google API key for accessing the Google Gemini LLM AI.
