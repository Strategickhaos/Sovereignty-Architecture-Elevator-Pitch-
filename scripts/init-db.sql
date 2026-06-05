-- SAGCO OS Database Schema
-- Version: 0.1.0
-- PostgreSQL 15+

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS sagco;
CREATE SCHEMA IF NOT EXISTS audit;

-- Set search path
SET search_path TO sagco, public;

-- ============================================
-- NODES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS sagco.nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_id VARCHAR(255) UNIQUE NOT NULL,
    layer VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 100,
    current_load INTEGER NOT NULL DEFAULT 0,
    health_score DECIMAL(3,2) NOT NULL DEFAULT 1.0,
    last_heartbeat TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::JSONB,
    
    CONSTRAINT chk_layer CHECK (layer IN ('sensory', 'cognitive', 'executive', 'motor')),
    CONSTRAINT chk_health CHECK (health_score >= 0.0 AND health_score <= 1.0),
    CONSTRAINT chk_load CHECK (current_load >= 0 AND current_load <= capacity)
);

CREATE INDEX idx_nodes_layer ON sagco.nodes(layer);
CREATE INDEX idx_nodes_health ON sagco.nodes(health_score);
CREATE INDEX idx_nodes_heartbeat ON sagco.nodes(last_heartbeat);
CREATE INDEX idx_nodes_metadata ON sagco.nodes USING GIN(metadata);

-- ============================================
-- TASKS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS sagco.tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id VARCHAR(255) UNIQUE NOT NULL,
    task_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    priority INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    assigned_node_id UUID REFERENCES sagco.nodes(id),
    result JSONB,
    dopamine_reward DECIMAL(10,4) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    CONSTRAINT chk_status CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    CONSTRAINT chk_priority CHECK (priority >= 0 AND priority <= 100)
);

CREATE INDEX idx_tasks_status ON sagco.tasks(status);
CREATE INDEX idx_tasks_type ON sagco.tasks(task_type);
CREATE INDEX idx_tasks_priority ON sagco.tasks(priority DESC);
CREATE INDEX idx_tasks_created ON sagco.tasks(created_at DESC);
CREATE INDEX idx_tasks_payload ON sagco.tasks USING GIN(payload);

-- ============================================
-- DOPAMINE REWARDS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS sagco.dopamine_rewards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID REFERENCES sagco.tasks(id) ON DELETE CASCADE,
    task_type VARCHAR(100) NOT NULL,
    reward_value DECIMAL(10,4) NOT NULL,
    execution_time DECIMAL(10,4) NOT NULL,
    quality_score DECIMAL(3,2) NOT NULL,
    success BOOLEAN NOT NULL,
    dopamine_level VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_dopamine_level CHECK (dopamine_level IN ('critical_high', 'high', 'neutral', 'low', 'critical_low'))
);

CREATE INDEX idx_rewards_task_type ON sagco.dopamine_rewards(task_type);
CREATE INDEX idx_rewards_created ON sagco.dopamine_rewards(created_at DESC);
CREATE INDEX idx_rewards_level ON sagco.dopamine_rewards(dopamine_level);

-- ============================================
-- ACADEMIC CONTEXTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS sagco.academic_contexts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    context_id VARCHAR(255) UNIQUE NOT NULL,
    course_code VARCHAR(100) NOT NULL,
    module VARCHAR(255) NOT NULL,
    learning_objectives TEXT[] NOT NULL,
    research_questions TEXT[],
    citations TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_contexts_course ON sagco.academic_contexts(course_code);

-- ============================================
-- EVENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS sagco.events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_name VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_events_name ON sagco.events(event_name);
CREATE INDEX idx_events_created ON sagco.events(created_at DESC);
CREATE INDEX idx_events_data ON sagco.events USING GIN(event_data);

-- ============================================
-- AUDIT LOG TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS audit.audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    old_data JSONB,
    new_data JSONB,
    changed_by VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_operation CHECK (operation IN ('INSERT', 'UPDATE', 'DELETE'))
);

CREATE INDEX idx_audit_table ON audit.audit_log(table_name);
CREATE INDEX idx_audit_created ON audit.audit_log(created_at DESC);

-- ============================================
-- VIEWS
-- ============================================

-- Node health summary
CREATE OR REPLACE VIEW sagco.v_node_health AS
SELECT 
    layer,
    COUNT(*) as total_nodes,
    COUNT(*) FILTER (WHERE health_score >= 0.8) as healthy_nodes,
    COUNT(*) FILTER (WHERE health_score < 0.5) as unhealthy_nodes,
    AVG(health_score) as avg_health_score,
    AVG((current_load::DECIMAL / capacity) * 100) as avg_utilization
FROM sagco.nodes
GROUP BY layer;

-- Task statistics
CREATE OR REPLACE VIEW sagco.v_task_statistics AS
SELECT 
    task_type,
    status,
    COUNT(*) as count,
    AVG(dopamine_reward) as avg_reward,
    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) as avg_execution_time
FROM sagco.tasks
WHERE completed_at IS NOT NULL
GROUP BY task_type, status;

-- Dopamine trends
CREATE OR REPLACE VIEW sagco.v_dopamine_trends AS
SELECT 
    task_type,
    DATE_TRUNC('hour', created_at) as hour,
    COUNT(*) as task_count,
    AVG(reward_value) as avg_reward,
    COUNT(*) FILTER (WHERE success = true) as success_count,
    COUNT(*) FILTER (WHERE success = false) as failure_count
FROM sagco.dopamine_rewards
GROUP BY task_type, DATE_TRUNC('hour', created_at)
ORDER BY hour DESC;

-- ============================================
-- FUNCTIONS
-- ============================================

-- Update node heartbeat
CREATE OR REPLACE FUNCTION sagco.update_node_heartbeat(p_node_id VARCHAR)
RETURNS VOID AS $$
BEGIN
    UPDATE sagco.nodes
    SET last_heartbeat = CURRENT_TIMESTAMP,
        updated_at = CURRENT_TIMESTAMP
    WHERE node_id = p_node_id;
END;
$$ LANGUAGE plpgsql;

-- Calculate average reward for task type
CREATE OR REPLACE FUNCTION sagco.get_avg_reward(p_task_type VARCHAR)
RETURNS DECIMAL AS $$
DECLARE
    avg_reward DECIMAL;
BEGIN
    SELECT AVG(reward_value)
    INTO avg_reward
    FROM sagco.dopamine_rewards
    WHERE task_type = p_task_type
    AND created_at > CURRENT_TIMESTAMP - INTERVAL '7 days';
    
    RETURN COALESCE(avg_reward, 0.0);
END;
$$ LANGUAGE plpgsql;

-- Audit trigger function
CREATE OR REPLACE FUNCTION audit.audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit.audit_log (table_name, operation, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit.audit_log (table_name, operation, old_data, new_data)
        VALUES (TG_TABLE_NAME, TG_OP, row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit.audit_log (table_name, operation, old_data)
        VALUES (TG_TABLE_NAME, TG_OP, row_to_json(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- TRIGGERS
-- ============================================

-- Auto-update timestamps
CREATE OR REPLACE FUNCTION sagco.update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER nodes_update_timestamp
    BEFORE UPDATE ON sagco.nodes
    FOR EACH ROW
    EXECUTE FUNCTION sagco.update_timestamp();

CREATE TRIGGER contexts_update_timestamp
    BEFORE UPDATE ON sagco.academic_contexts
    FOR EACH ROW
    EXECUTE FUNCTION sagco.update_timestamp();

-- Audit triggers
CREATE TRIGGER nodes_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON sagco.nodes
    FOR EACH ROW
    EXECUTE FUNCTION audit.audit_trigger();

CREATE TRIGGER tasks_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON sagco.tasks
    FOR EACH ROW
    EXECUTE FUNCTION audit.audit_trigger();

-- ============================================
-- INITIAL DATA
-- ============================================

-- Insert default academic context
INSERT INTO sagco.academic_contexts (context_id, course_code, module, learning_objectives, research_questions)
VALUES (
    'cyber-psy-620',
    'CYBER-PSY-620',
    'Cognitive Architecture & Distributed Systems',
    ARRAY[
        'Understand distributed cognitive systems',
        'Implement reward-based learning mechanisms',
        'Design layered processing architectures',
        'Apply sovereignty principles to system design'
    ],
    ARRAY[
        'How can dopamine-inspired reward systems improve distributed task processing?',
        'What are the optimal layer architectures for cognitive OS?',
        'How does academic context integration improve learning outcomes?'
    ]
) ON CONFLICT (context_id) DO NOTHING;

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA sagco TO sagco;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA sagco TO sagco;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA sagco TO sagco;
GRANT SELECT ON ALL TABLES IN SCHEMA audit TO sagco;

-- Completed
DO $$ 
BEGIN
    RAISE NOTICE 'SAGCO database schema initialized successfully';
END $$;
