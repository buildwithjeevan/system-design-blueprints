#!/bin/bash

# --- Configuration ---
MODULE_NAME="01-api-gateway-microservices"

echo "🚀 Setting up module: $MODULE_NAME ..."

# --- Folder Structure ---
mkdir -p "$MODULE_NAME/user_service"
mkdir -p "$MODULE_NAME/order_service"

# --- Virtual Environment Setup ---
if [ ! -d "venv" ]; then
  echo "🧱 Creating Python virtual environment..."
  python3 -m venv venv
else
  echo "✅ Virtual environment already exists, skipping creation."
fi

echo "📦 Activating virtual environment and installing dependencies..."
# Activate venv in a POSIX-compatible way
# (If using Windows native shell, run venv\Scripts\activate manually)
source venv/bin/activate || { echo "Failed to activate venv. Are you on Windows?"; exit 1; }
pip install --upgrade pip
pip install fastapi uvicorn requests

# --- Freeze requirements ---
pip freeze > requirements.txt
deactivate

# --- Module README ---
cat << 'EOF' > "$MODULE_NAME/README.md"
# 🧩 API Gateway + Microservices (Python FastAPI)

### 📘 Problem
How can we route client requests to multiple backend services without exposing them directly?

### 🏗️ Architecture
- **API Gateway** routes requests to:
  - `UserService` → fetch user info
  - `OrderService` → fetch order list
- Gateway aggregates both responses into one unified output.

### 🧩 Diagram
```mermaid
graph TD
Client -->|HTTP Request| APIGateway
APIGateway -->|/user| UserService
APIGateway -->|/orders| OrderService