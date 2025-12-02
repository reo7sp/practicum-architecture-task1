package handlers

import (
	"context"
	"net/http"
	"strconv"

	"sensors-service/db"
	"sensors-service/models"

	"github.com/gin-gonic/gin"
)

type SensorHandler struct {
	DB *db.DB
}

func NewSensorHandler(db *db.DB) *SensorHandler {
	return &SensorHandler{
		DB: db,
	}
}

func (h *SensorHandler) RegisterRoutes(router *gin.RouterGroup) {
	sensors := router.Group("/sensors")
	{
		sensors.GET("", h.GetSensors)
		sensors.GET("/:id", h.GetSensorByID)
		sensors.POST("", h.CreateSensor)
		sensors.PUT("/:id", h.UpdateSensor)
		sensors.DELETE("/:id", h.DeleteSensor)
		sensors.PATCH("/:id/value", h.UpdateSensorValue)
	}
}

func (h *SensorHandler) RegisterV1DeviceRoutes(router *gin.RouterGroup) {
	v1 := router.Group("/devices/:manufacturer_id/:device_id/sensors")
	{
		v1.GET("", h.GetDeviceSensors)
		v1.GET("/:sensor_id", h.GetSensorHistory)
	}
}

func (h *SensorHandler) GetSensors(c *gin.Context) {
	sensors, err := h.DB.GetSensors(context.Background())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, sensors)
}

func (h *SensorHandler) GetSensorByID(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid sensor ID"})
		return
	}

	sensor, err := h.DB.GetSensorByID(context.Background(), id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Sensor not found"})
		return
	}

	c.JSON(http.StatusOK, sensor)
}

func (h *SensorHandler) CreateSensor(c *gin.Context) {
	var sensorCreate models.SensorCreate
	if err := c.ShouldBindJSON(&sensorCreate); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	sensor, err := h.DB.CreateSensor(context.Background(), sensorCreate)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, sensor)
}

func (h *SensorHandler) UpdateSensor(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid sensor ID"})
		return
	}

	var sensorUpdate models.SensorUpdate
	if err := c.ShouldBindJSON(&sensorUpdate); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	sensor, err := h.DB.UpdateSensor(context.Background(), id, sensorUpdate)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, sensor)
}

func (h *SensorHandler) DeleteSensor(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid sensor ID"})
		return
	}

	err = h.DB.DeleteSensor(context.Background(), id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Sensor deleted successfully"})
}

func (h *SensorHandler) UpdateSensorValue(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid sensor ID"})
		return
	}

	var request struct {
		Value  float64 `json:"value" binding:"required"`
		Status string  `json:"status" binding:"required"`
	}

	if err := c.ShouldBindJSON(&request); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	err = h.DB.UpdateSensorValue(context.Background(), id, request.Value, request.Status)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Sensor value updated successfully"})
}

func (h *SensorHandler) GetDeviceSensors(c *gin.Context) {
	manufacturerID := c.Param("manufacturer_id")
	deviceID := c.Param("device_id")

	offset, _ := strconv.Atoi(c.DefaultQuery("offset", "0"))
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "10"))

	v2IDs, err := h.DB.GetSensorV2IDsByDevice(context.Background(), manufacturerID, deviceID, offset, limit)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Device not found"})
		return
	}

	result := make([]map[string]string, len(v2IDs))
	for i, v2ID := range v2IDs {
		result[i] = map[string]string{
			"sensor_id": v2ID.SensorID,
		}
	}

	c.JSON(http.StatusOK, result)
}

func (h *SensorHandler) GetSensorHistory(c *gin.Context) {
	manufacturerID := c.Param("manufacturer_id")
	deviceID := c.Param("device_id")
	sensorID := c.Param("sensor_id")

	sensorDBID, err := h.DB.GetSensorIDByV2ID(context.Background(), manufacturerID, deviceID, sensorID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Sensor not found"})
		return
	}

	sensor, err := h.DB.GetSensorByID(context.Background(), sensorDBID)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Sensor not found"})
		return
	}

	entry := models.SensorHistoryEntry{
		Name:      sensor.Name,
		Type:      string(sensor.Type),
		Location:  sensor.Location,
		Value:     sensor.Value,
		Unit:      sensor.Unit,
		Status:    sensor.Status,
		Timestamp: sensor.LastUpdated,
	}

	c.JSON(http.StatusOK, []models.SensorHistoryEntry{entry})
}
