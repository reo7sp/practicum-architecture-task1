package models

import (
	"time"
)

type SensorType string

const (
	Temperature SensorType = "temperature"
)

type Sensor struct {
	ID          int        `json:"id"`
	Name        string     `json:"name"`
	Type        SensorType `json:"type"`
	Location    string     `json:"location"`
	Value       float64    `json:"value"`
	Unit        string     `json:"unit"`
	Status      string     `json:"status"`
	LastUpdated time.Time  `json:"last_updated"`
	CreatedAt   time.Time  `json:"created_at"`
}

type SensorCreate struct {
	Name     string     `json:"name" binding:"required"`
	Type     SensorType `json:"type" binding:"required"`
	Location string     `json:"location" binding:"required"`
	Unit     string     `json:"unit"`
}

type SensorUpdate struct {
	Name     string     `json:"name"`
	Type     SensorType `json:"type"`
	Location string     `json:"location"`
	Value    *float64   `json:"value"`
	Unit     string     `json:"unit"`
	Status   string     `json:"status"`
}

type SensorV2ID struct {
	ManufacturerID string `json:"manufacturer_id"`
	DeviceID       string `json:"device_id"`
	SensorID       string `json:"sensor_id"`
	ID             int    `json:"id"`
}

type SensorHistoryEntry struct {
	Name      string    `json:"name"`
	Type      string    `json:"type"`
	Location  string    `json:"location"`
	Value     float64   `json:"value"`
	Unit      string    `json:"unit"`
	Status    string    `json:"status"`
	Timestamp time.Time `json:"timestamp"`
}

type SensorReadingEvent struct {
	ManufacturerID string    `json:"manufacturer_id"`
	DeviceID       string    `json:"device_id"`
	SensorID       string    `json:"sensor_id"`
	Value          float64   `json:"value"`
	Unit           string    `json:"unit"`
	Status         string    `json:"status"`
	Timestamp      time.Time `json:"timestamp"`
}
