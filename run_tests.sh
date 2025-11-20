#!/bin/bash
# Script to run all tests for EvoForge

set -e

echo "==================================="
echo "EvoForge Test Suite"
echo "==================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Installing test dependencies...${NC}"
pip install -q -r requirements-test.txt

echo ""
echo -e "${YELLOW}Running Unit Tests...${NC}"
pytest tests/unit/ -v --tb=short || echo -e "${RED}Some unit tests failed${NC}"

echo ""
echo -e "${YELLOW}Running Integration Tests...${NC}"
pytest tests/integration/ -v --tb=short || echo -e "${RED}Some integration tests failed${NC}"

echo ""
echo -e "${GREEN}Test run complete!${NC}"
echo ""
echo "To run specific test files:"
echo "  pytest tests/unit/test_sandbox.py -v"
echo "  pytest tests/unit/test_evolution_engine.py -v"
echo "  pytest tests/integration/test_api.py -v"
echo ""
echo "To run with coverage:"
echo "  pytest --cov=evolution-engine --cov=backend tests/"
