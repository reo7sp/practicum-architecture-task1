package main

import (
	"encoding/json"
	"net/http"
	"strings"
)

type SessionCheckResponse struct {
	UserID string `json:"user_id"`
}

type ErrorResponse struct {
	Error string `json:"error"`
}

type HTTPError struct {
	StatusCode int
	Message    string
}

func (e *HTTPError) Error() string {
	return e.Message
}

func validateToken(token string, authServiceURL string, httpClient *http.Client) (string, error) {
	req, err := http.NewRequest("POST", authServiceURL+"/api/v1/sessions/check", nil)
	if err != nil {
		return "", err
	}
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")

	resp, err := httpClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		var errorResp ErrorResponse
		if err := json.NewDecoder(resp.Body).Decode(&errorResp); err == nil {
			return "", &HTTPError{StatusCode: resp.StatusCode, Message: errorResp.Error}
		}
		return "", &HTTPError{StatusCode: resp.StatusCode, Message: "Token validation failed"}
	}

	var sessionResp SessionCheckResponse
	if err := json.NewDecoder(resp.Body).Decode(&sessionResp); err != nil {
		return "", err
	}

	return sessionResp.UserID, nil
}

func authMiddleware(authServiceURL string, httpClient *http.Client) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			authHeader := r.Header.Get("Authorization")
			if authHeader == "" {
				http.Error(w, "Authorization header required", http.StatusUnauthorized)
				return
			}

			parts := strings.Split(authHeader, " ")
			if len(parts) != 2 || parts[0] != "Bearer" {
				http.Error(w, "Invalid authorization header format", http.StatusUnauthorized)
				return
			}

			token := parts[1]
			userID, err := validateToken(token, authServiceURL, httpClient)
			if err != nil {
				if httpErr, ok := err.(*HTTPError); ok {
					w.Header().Set("Content-Type", "application/json")
					w.WriteHeader(httpErr.StatusCode)
					json.NewEncoder(w).Encode(ErrorResponse{Error: httpErr.Message})
					return
				}
				http.Error(w, "Token validation failed", http.StatusInternalServerError)
				return
			}

			r.Header.Set("X-User-ID", userID)
			next.ServeHTTP(w, r)
		})
	}
}
