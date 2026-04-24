CREATE TABLE IF NOT EXISTS financial.goals (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    goal_amount NUMERIC(12,2) NOT NULL,
    current_progress NUMERIC(12,2) NOT NULL DEFAULT 0,
    monthly_contribution NUMERIC(12,2) NOT NULL DEFAULT 0,
    target_month SMALLINT CHECK (target_month BETWEEN 1 AND 12),
    target_year SMALLINT,
    created_at TIMESTAMPTZ DEFAULT now()
);
