#!/bin/bash

echo "🔍 Vérification Black..."
black --check src/ tests/ || echo "❌ Black a trouvé des erreurs"

echo "🔍 Vérification Isort..."
isort --check-only src/ tests/ || echo "❌ Isort a trouvé des erreurs"

echo "🔍 Vérification Mypy..."
mypy || echo "❌ Mypy a trouvé des erreurs"
