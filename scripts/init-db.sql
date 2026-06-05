-- SAGCO Database Initialization Script
-- PostgreSQL schema and initial data

-- =============================================================================
-- DATABASE SETUP
-- =============================================================================

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- =============================================================================
-- TABLES
-- =============================================================================

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    effort INTEGER DEFAULT 5,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    deadline TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT check_priority CHECK (priority IN ('critical', 'high', 'medium', 'low', 'background')),
    CONSTRAINT check_status CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),
    CONSTRAINT check_effort CHECK (effort >= 1 AND effort <= 10)
);

-- Academic metrics table
CREATE TABLE IF NOT EXISTS academic_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    study_hours DECIMAL(5,2) DEFAULT 0.0,
    assignments_completed INTEGER DEFAULT 0,
    discussion_posts INTEGER DEFAULT 0,
    quiz_scores JSONB DEFAULT '[]'::jsonb,
    current_gpa DECIMAL(3,2),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Cognitive layer activity table
CREATE TABLE IF NOT EXISTS cognitive_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    layer VARCHAR(20) NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    duration_seconds INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT check_layer CHECK (layer IN ('reflexive', 'tactical', 'strategic', 'sovereign'))
);

-- Dopamine tracking table
CREATE TABLE IF NOT EXISTS dopamine_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    level VARCHAR(20) NOT NULL,
    score INTEGER,
    trigger VARCHAR(100),
    notes TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT check_level CHECK (level IN ('depleted', 'baseline', 'elevated', 'flow'))
);

-- Performance history table
CREATE TABLE IF NOT EXISTS performance_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2),
    metric_unit VARCHAR(20),
    metadata JSONB DEFAULT '{}'::jsonb,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- System events table
CREATE TABLE IF NOT EXISTS system_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB DEFAULT '{}'::jsonb,
    severity VARCHAR(20) DEFAULT 'info',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT check_severity CHECK (severity IN ('debug', 'info', 'warning', 'error', 'critical'))
);

-- =============================================================================
-- INDEXES
-- =============================================================================

-- Task indexes
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_deadline ON tasks(deadline);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_tasks_metadata ON tasks USING gin(metadata);

-- Academic metrics indexes
CREATE INDEX idx_academic_metrics_date ON academic_metrics(date DESC);
CREATE INDEX idx_academic_metrics_gpa ON academic_metrics(current_gpa);

-- Cognitive activity indexes
CREATE INDEX idx_cognitive_activity_layer ON cognitive_activity(layer);
CREATE INDEX idx_cognitive_activity_timestamp ON cognitive_activity(timestamp DESC);

-- Dopamine tracking indexes
CREATE INDEX idx_dopamine_tracking_level ON dopamine_tracking(level);
CREATE INDEX idx_dopamine_tracking_timestamp ON dopamine_tracking(timestamp DESC);

-- Performance history indexes
CREATE INDEX idx_performance_history_metric ON performance_history(metric_name);
CREATE INDEX idx_performance_history_timestamp ON performance_history(timestamp DESC);

-- System events indexes
CREATE INDEX idx_system_events_type ON system_events(event_type);
CREATE INDEX idx_system_events_severity ON system_events(severity);
CREATE INDEX idx_system_events_timestamp ON system_events(timestamp DESC);

-- =============================================================================
-- FUNCTIONS
-- =============================================================================

-- Update timestamp function
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Task completion function
CREATE OR REPLACE FUNCTION complete_task(task_id UUID)
RETURNS VOID AS $$
BEGIN
    UPDATE tasks 
    SET status = 'completed', 
        completed_at = NOW(),
        updated_at = NOW()
    WHERE id = task_id;
    
    -- Log system event
    INSERT INTO system_events (event_type, event_data, severity)
    VALUES ('task_completed', json_build_object('task_id', task_id), 'info');
END;
$$ LANGUAGE plpgsql;

-- Calculate GPA function
CREATE OR REPLACE FUNCTION calculate_gpa(scores JSONB)
RETURNS DECIMAL(3,2) AS $$
DECLARE
    total DECIMAL(10,2) := 0;
    count INTEGER := 0;
    score JSONB;
BEGIN
    FOR score IN SELECT jsonb_array_elements(scores)
    LOOP
        total := total + (score::text)::DECIMAL;
        count := count + 1;
    END LOOP;
    
    IF count = 0 THEN
        RETURN 0.00;
    END IF;
    
    RETURN ROUND((total / count / 100.0 * 4.0)::NUMERIC, 2);
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- TRIGGERS
-- =============================================================================

-- Update timestamp triggers
CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_academic_metrics_updated_at
    BEFORE UPDATE ON academic_metrics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- =============================================================================
-- INITIAL DATA
-- =============================================================================

-- Insert initial academic metrics record
INSERT INTO academic_metrics (date, study_hours, current_gpa, notes)
VALUES (CURRENT_DATE, 0.0, 4.0, 'SAGCO system initialized')
ON CONFLICT DO NOTHING;

-- Insert system startup event
INSERT INTO system_events (event_type, event_data, severity)
VALUES ('system_initialized', 
        json_build_object('version', '0.1.0', 'timestamp', NOW()), 
        'info');

-- Insert sample tasks for demonstration
INSERT INTO tasks (title, description, priority, effort, deadline, metadata)
VALUES 
    ('Complete CYBER-PSY-620 Discussion Post', 
     'Write initial post and respond to 2 peers', 
     'critical', 
     3, 
     NOW() + INTERVAL '16 hours',
     '{"type": "academic", "course": "CYBER-PSY-620"}'::jsonb),
    
    ('Review Kubernetes manifests', 
     'Audit security settings in SAGCO K8s config', 
     'high', 
     4, 
     NOW() + INTERVAL '2 days',
     '{"type": "devops", "area": "security"}'::jsonb),
    
    ('Update SAGCO documentation', 
     'Document new dopamine tracking feature', 
     'medium', 
     2, 
     NOW() + INTERVAL '1 week',
     '{"type": "documentation"}'::jsonb);

-- =============================================================================
-- VIEWS
-- =============================================================================

-- Active tasks view
CREATE OR REPLACE VIEW active_tasks AS
SELECT 
    id,
    title,
    priority,
    effort,
    deadline,
    EXTRACT(EPOCH FROM (deadline - NOW())) / 3600 AS hours_until_deadline,
    created_at
FROM tasks
WHERE status = 'pending'
ORDER BY priority DESC, deadline ASC;

-- Academic performance view
CREATE OR REPLACE VIEW academic_performance AS
SELECT 
    date,
    study_hours,
    assignments_completed,
    discussion_posts,
    current_gpa,
    (SELECT AVG(current_gpa) FROM academic_metrics WHERE date >= CURRENT_DATE - INTERVAL '30 days') AS gpa_30_day_avg
FROM academic_metrics
ORDER BY date DESC;

-- System health view
CREATE OR REPLACE VIEW system_health AS
SELECT 
    COUNT(*) FILTER (WHERE event_type = 'error' AND timestamp > NOW() - INTERVAL '1 hour') AS errors_last_hour,
    COUNT(*) FILTER (WHERE event_type = 'warning' AND timestamp > NOW() - INTERVAL '1 hour') AS warnings_last_hour,
    COUNT(*) FILTER (WHERE severity = 'critical' AND timestamp > NOW() - INTERVAL '24 hours') AS critical_events_24h
FROM system_events;

-- =============================================================================
-- PERMISSIONS
-- =============================================================================

-- Grant permissions to sagco user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sagco;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sagco;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO sagco;

-- =============================================================================
-- MAINTENANCE
-- =============================================================================

-- Vacuum and analyze
VACUUM ANALYZE;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'SAGCO database initialization complete!';
END $$;
