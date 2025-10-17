.PHONY: db-push db-pull db-init db-load help

db-init:
	@echo "Creating initial fixtures..."
	python manage.py dumpdata --exclude=auth --exclude=contenttypes --exclude=sessions --exclude=admin.logentry --indent=2 -o fixtures/realestate_data.json
	@echo "Fixtures created! Now commit and push: git add fixtures/ && git commit -m 'Add initial fixtures'"

db-push:
	@echo "Checking for updates..."
	@git fetch origin
	@if git status | grep -q "behind"; then \
		echo "Your repository is behind. Run 'make db-pull' first!"; \
		exit 1; \
	fi
	@echo "Updating fixtures..."
	python manage.py dumpdata --exclude=auth --exclude=contenttypes --exclude=sessions --exclude=admin.logentry --indent=2 -o fixtures/realestate_data.json
	git add fixtures/realestate_data.json
	git commit -m "Update database fixtures"
	git push
	@echo "Fixtures updated and pushed! Notify your team."

db-load:
	@echo "Loading fixtures into database..."
	python manage.py migrate
	python manage.py loaddata realestate_data.json

db-pull:
	@echo "Pulling latest data..."
	git pull
	@echo "Updating database..."
	python manage.py migrate
	python manage.py loaddata realestate_data.json

help:
	@echo "Available commands:"
	@echo "  make db-init  - Create initial fixtures from your DB"
	@echo "  make db-pull  - Get latest database"
	@echo "  make db-push  - Share your database changes"
	@echo "  make db-load  - Load fixtures into database"
	@echo "  make help     - Show this help"