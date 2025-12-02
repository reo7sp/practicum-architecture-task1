package main

import (
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"time"

	"github.com/gorilla/mux"
)

var (
	authServiceURL        = os.Getenv("AUTH_SERVICE_URL")
	devicesServiceURL     = os.Getenv("DEVICES_SERVICE_URL")
	actionsServiceURL     = os.Getenv("ACTIONS_SERVICE_URL")
	automationsServiceURL = os.Getenv("AUTOMATIONS_SERVICE_URL")
	sensorsServiceURL     = os.Getenv("SENSORS_SERVICE_URL")
	httpClient            = &http.Client{
		Timeout: 5 * time.Second,
	}
)

func init() {
	if authServiceURL == "" {
		authServiceURL = "http://auth-service:5001"
	}
	if devicesServiceURL == "" {
		devicesServiceURL = "http://devices-service:5002"
	}
	if actionsServiceURL == "" {
		actionsServiceURL = "http://actions-service:5003"
	}
	if automationsServiceURL == "" {
		automationsServiceURL = "http://automations-service:5004"
	}
	if sensorsServiceURL == "" {
		sensorsServiceURL = "http://sensors-service:5005"
	}
}

func createReverseProxy(targetURL string) *httputil.ReverseProxy {
	target, _ := url.Parse(targetURL)
	return httputil.NewSingleHostReverseProxy(target)
}

func main() {
	authProxy := createReverseProxy(authServiceURL)
	devicesProxy := createReverseProxy(devicesServiceURL)
	actionsProxy := createReverseProxy(actionsServiceURL)
	automationsProxy := createReverseProxy(automationsServiceURL)
	sensorsProxy := createReverseProxy(sensorsServiceURL)

	r := mux.NewRouter()
	r.PathPrefix("/api/v1/users").Handler(authProxy)
	r.PathPrefix("/api/v1/sessions").Handler(authProxy)
	r.PathPrefix("/api/v1/devices/{manufacturer_id}/{device_id}/actions").Handler(authMiddleware(authServiceURL, httpClient)(actionsProxy))
	r.PathPrefix("/api/v1/devices/{manufacturer_id}/{device_id}/sensors").Handler(authMiddleware(authServiceURL, httpClient)(sensorsProxy))
	r.PathPrefix("/api/v1/devices").Handler(authMiddleware(authServiceURL, httpClient)(devicesProxy))
	r.PathPrefix("/api/v1/scenarios").Handler(authMiddleware(authServiceURL, httpClient)(automationsProxy))
	r.PathPrefix("/api/v1/sensors").Handler(authMiddleware(authServiceURL, httpClient)(sensorsProxy))

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Printf("API Gateway starting on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, r))
}
