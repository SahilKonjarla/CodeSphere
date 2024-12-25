CREATE TABLE user_logs (
    id SERIAL PRIMARY KEY,                  -- Unique identifier for each log entry
    user_id VARCHAR(255) NOT NULL,          -- Identifier for the user (e.g., user ID or session ID)
    agent VARCHAR(50) NOT NULL,             -- The agent that handled the request (e.g., debug, optimize, document)
    request JSONB NOT NULL,                 -- JSON representation of the user's request (e.g., code snippet, options)
    response JSONB NOT NULL,                -- JSON representation of the agent's response (e.g., suggestions, issues)
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp of the interaction, defaults to current time
);
