#!/bin/bash
echo "🧪 Lancement des tests..."
pytest tests/ --cov=itcaa_ai_offline --cov-report=term-missing
