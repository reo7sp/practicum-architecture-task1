package services

import (
	"context"
	"encoding/json"
	"log"

	"sensors-service/db"
	"sensors-service/models"

	"github.com/segmentio/kafka-go"
)

type KafkaConsumer struct {
	reader *kafka.Reader
	db     *db.DB
}

func NewKafkaConsumer(brokers []string, topic, groupID string, db *db.DB) *KafkaConsumer {
	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:  brokers,
		Topic:    topic,
		GroupID:  groupID,
		MinBytes: 10e3,
		MaxBytes: 10e6,
	})

	return &KafkaConsumer{
		reader: reader,
		db:     db,
	}
}

func (kc *KafkaConsumer) Start(ctx context.Context) {
	for {
		select {
		case <-ctx.Done():
			log.Println("Stopping Kafka consumer...")
			return
		default:
			msg, err := kc.reader.FetchMessage(ctx)
			if err != nil {
				log.Printf("Error fetching message: %v\n", err)
				continue
			}

			var event models.SensorReadingEvent
			if err := json.Unmarshal(msg.Value, &event); err != nil {
				log.Printf("Error unmarshaling message: %v\n", err)
				kc.reader.CommitMessages(ctx, msg)
				continue
			}

			sensorID, err := kc.db.GetSensorIDByV2ID(ctx, event.ManufacturerID, event.DeviceID, event.SensorID)
			if err != nil {
				log.Printf("Error getting sensor ID: %v\n", err)
				kc.reader.CommitMessages(ctx, msg)
				continue
			}

			if err := kc.db.SaveSensorReading(ctx, sensorID, event.Value, event.Status, event.Timestamp); err != nil {
				log.Printf("Error saving sensor reading: %v\n", err)
				kc.reader.CommitMessages(ctx, msg)
				continue
			}

			log.Printf("Processed sensor reading: %s/%s/%s = %f\n",
				event.ManufacturerID, event.DeviceID, event.SensorID, event.Value)

			if err := kc.reader.CommitMessages(ctx, msg); err != nil {
				log.Printf("Error committing message: %v\n", err)
			}
		}
	}
}

func (kc *KafkaConsumer) Close() error {
	return kc.reader.Close()
}
