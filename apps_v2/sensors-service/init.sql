CREATE TABLE IF NOT EXISTS sensors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    value FLOAT DEFAULT 0,
    unit VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'inactive',
    last_updated TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sensor_v2_ids (
    manufacturer_id VARCHAR(100) NOT NULL,
    device_id VARCHAR(100) NOT NULL,
    sensor_id VARCHAR(100) NOT NULL,
    id INTEGER NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    PRIMARY KEY (manufacturer_id, device_id, sensor_id)
);

CREATE INDEX IF NOT EXISTS idx_sensors_type ON sensors(type);
CREATE INDEX IF NOT EXISTS idx_sensors_location ON sensors(location);
CREATE INDEX IF NOT EXISTS idx_sensors_status ON sensors(status);
CREATE INDEX IF NOT EXISTS idx_sensor_v2_ids_id ON sensor_v2_ids(id);
