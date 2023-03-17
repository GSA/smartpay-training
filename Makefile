.PHONY: list start frontend backend db-up db-down test

list:		# List all available make tasks
	@echo "Usage: make TASK"
	@echo
	@echo "Available tasks:"
	@grep '^[^#[:space:]].*:' Makefile | grep -v '^\..*'

start:		# Start development servers (frontend + backend)
	@(trap "kill 0" SIGINT; make frontend & make backend)

frontend:	# Start Vue frontend
	cd smartpay-training-quiz && npm run dev -- --clearScreen=false

backend:	# Start FastAPI backend
	uvicorn training.main:app --reload

db-start:	# Start Redis and PostgreSQL containers
	@docker-compose up -d

db-stop:	# Stop Redis and PostgreSQL containers
	@docker-compose stop

test:		# Run tests
	@pytest
