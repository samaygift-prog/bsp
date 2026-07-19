-- ==========================================
-- BSP Personal Response Database
-- Version 1.0
-- ==========================================

CREATE TABLE responses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT NOT NULL,

    mobile TEXT,

    problem TEXT,

    medical_history TEXT,

    talent TEXT,

    future_plan TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP

);