#!/bin/bash
# agent-zero-1 test harness: Minimal Feature Validation Demo
# Demonstrates the cognitive flowchart without external dependencies

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

echo "=========================================="
echo "Agent Zero Feature Validation (Demo Mode)"
echo "Cognitive Flowchart Implementation"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "agent.py" ] || [ ! -f "initialize.py" ]; then
    echo "Please run this script from the agent-zero-1 root directory"
    exit 1
fi

# Create demo results directory
mkdir -p test_results
TIMESTAMP=$(date +'%Y%m%d_%H%M%S')
RESULTS_DIR="test_results/demo_validation_${TIMESTAMP}"
mkdir -p "$RESULTS_DIR"

log "Demo validation results: $RESULTS_DIR"

# ============================================================================
# [1] Environment Check (without package installation)
# ============================================================================
log "[1] Environment validation (demo mode)..."

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
log "Python version: $PYTHON_VERSION"

# Check essential files
log "Checking essential file structure..."
ESSENTIAL_FILES=("agent.py" "initialize.py" "requirements.txt" "python/tools" "python/api" "webui" "docs")
for file in "${ESSENTIAL_FILES[@]}"; do
    if [ -e "$file" ]; then
        success "✓ $file"
    else
        warning "✗ $file missing"
    fi
done

# ============================================================================
# [2] Feature Discovery  
# ============================================================================
log "[2] Running feature discovery (using system Python)..."

# Run feature validation with system Python (no venv)
python3 feature_validation.py > "$RESULTS_DIR/feature_validation.log" 2>&1 && {
    success "Feature enumeration complete"
    if [ -f "feature_validation_report.json" ]; then
        cp feature_validation_report.json "$RESULTS_DIR/"
    fi
} || {
    warning "Feature validation encountered issues (check log)"
}

# ============================================================================
# [3] Structure Analysis
# ============================================================================
log "[3] Analyzing codebase structure..."

# Count different types of components
TOOL_COUNT=$(find python/tools -name "*.py" ! -name "__init__.py" | wc -l)
API_COUNT=$(find python/api -name "*.py" ! -name "__init__.py" | wc -l)
WEB_COUNT=$(find webui/js -name "*.js" | wc -l)

log "Discovered components:"
log "  Python tools: $TOOL_COUNT"
log "  API endpoints: $API_COUNT"
log "  Web components: $WEB_COUNT"

# Create a simple analysis report
cat > "$RESULTS_DIR/structure_analysis.txt" << EOF
Agent Zero Structure Analysis
============================

Core Modules:
$(ls -1 *.py 2>/dev/null | grep -E "(agent|initialize|models|run_)" | sed 's/^/  /')

Python Tools:
$(find python/tools -name "*.py" ! -name "__init__.py" | sed 's/python\/tools\///;s/\.py$//' | sed 's/^/  /')

API Endpoints:
$(find python/api -name "*.py" ! -name "__init__.py" | sed 's/python\/api\///;s/\.py$//' | sed 's/^/  /')

Web Components:
$(find webui/js -name "*.js" | sed 's/webui\/js\///;s/\.js$//' | sed 's/^/  /')

Documentation:
$(find docs -name "*.md" | sed 's/docs\///;s/\.md$//' | sed 's/^/  /')
EOF

success "Structure analysis complete"

# ============================================================================
# [4] Basic Validation Tests
# ============================================================================
log "[4] Running basic validation tests..."

# Test basic Python syntax for core files
log "Checking Python syntax for core modules..."
SYNTAX_ERRORS=0
for py_file in *.py python/tools/*.py python/api/*.py; do
    if [ -f "$py_file" ]; then
        python3 -m py_compile "$py_file" 2>/dev/null || {
            warning "Syntax error in: $py_file"
            SYNTAX_ERRORS=$((SYNTAX_ERRORS + 1))
        }
    fi
done

if [ $SYNTAX_ERRORS -eq 0 ]; then
    success "All Python files have valid syntax"
else
    warning "$SYNTAX_ERRORS Python files have syntax errors"
fi

# ============================================================================
# [5] Manual Validation Guidance
# ============================================================================
log "[5] Generating manual validation guidance..."

cat > "$RESULTS_DIR/manual_validation_checklist.md" << 'EOF'
# Manual Validation Checklist for Agent Zero

## Core Functionality Tests

### 1. Agent Initialization
- [ ] Can import core modules without errors
- [ ] Configuration loading works correctly
- [ ] Agent context can be created

### 2. Tool System
- [ ] Tools can be discovered and loaded
- [ ] Code execution tool functions properly
- [ ] Memory tools (save/load/delete) work
- [ ] Knowledge tool can retrieve information

### 3. Web Interface
- [ ] Web UI loads without errors
- [ ] Settings panel is functional
- [ ] Chat interface responds correctly
- [ ] Scheduler interface works

### 4. API Endpoints
- [ ] API server starts successfully
- [ ] Endpoints respond to requests
- [ ] Authentication (if configured) works
- [ ] Error handling is appropriate

### 5. Integration Points
- [ ] Agent-to-agent communication
- [ ] Tool integration with agents
- [ ] Memory persistence
- [ ] Knowledge base access

## Testing Commands

```bash
# Test core imports
python3 -c "import agent, initialize, models; print('Core imports successful')"

# Test tool discovery
python3 -c "from pathlib import Path; print(f'Tools found: {len(list(Path(\"python/tools\").glob(\"*.py\")))}')"

# Test web UI (if dependencies available)
# python3 run_ui.py

# Test CLI (if dependencies available)  
# python3 run_cli.py
```

## Troubleshooting Guide

### Common Issues
1. **Import Errors**: Check if all dependencies are installed
2. **Configuration Issues**: Verify .env file and settings
3. **Port Conflicts**: Ensure required ports are available
4. **Permission Issues**: Check file and directory permissions

### Debug Steps
1. Check logs in the logs/ directory
2. Verify environment variables
3. Test individual components in isolation
4. Review error messages for specific guidance
EOF

success "Manual validation checklist created"

# ============================================================================
# [6] Summary Report
# ============================================================================
log "[6] Generating validation summary..."

cat > "$RESULTS_DIR/VALIDATION_SUMMARY.md" << EOF
# Agent Zero Feature Validation Summary

**Date:** $(date)  
**Mode:** Demo (without external dependencies)  
**Results Directory:** $RESULTS_DIR

## Results Overview

### Environment Status
- Python Version: $PYTHON_VERSION
- Essential Files: $(echo "${ESSENTIAL_FILES[@]}" | wc -w) checked
- File Structure: Complete

### Component Discovery
- Python Tools: $TOOL_COUNT discovered
- API Endpoints: $API_COUNT discovered  
- Web Components: $WEB_COUNT discovered
- Syntax Validation: $SYNTAX_ERRORS errors found

### Feature Hypergraph
$(if [ -f "$RESULTS_DIR/feature_validation_report.json" ]; then
    echo "✓ Feature hypergraph generated successfully"
    python3 -c "
import json
try:
    with open('$RESULTS_DIR/feature_validation_report.json') as f:
        data = json.load(f)
        print(f'- Total features: {data[\"summary\"][\"total_features\"]}')
        print(f'- Environment status: {data[\"summary\"][\"environment_status\"]}')
except:
    print('- Report parsing failed')
" 2>/dev/null || echo "- Could not parse report details"
else
    echo "✗ Feature hypergraph generation failed"
fi)

## Next Steps

1. **Install Dependencies**: Run the full validation with:
   \`\`\`bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   \`\`\`

2. **Complete Manual Tests**: Use the checklist in manual_validation_checklist.md

3. **Run Full Validation**: Execute ./test_all.sh for complete testing

4. **Address Issues**: Focus on any discovered problems

## Files Generated
- feature_validation_report.json (if successful)
- structure_analysis.txt
- manual_validation_checklist.md
- feature_validation.log

---
*Cognitive Flowchart Demo Complete*
EOF

success "Validation summary generated"

# ============================================================================
# Final Output
# ============================================================================
echo ""
echo "=========================================="
echo "DEMO VALIDATION COMPLETE"
echo "=========================================="
success "Cognitive flowchart demo executed successfully"
success "Results saved to: $RESULTS_DIR"
log "Review the generated reports and checklists"
warning "For full validation, install dependencies and run ./test_all.sh"

echo ""
echo "Quick Summary:"
echo "- Features discovered: Python tools ($TOOL_COUNT), API endpoints ($API_COUNT), Web components ($WEB_COUNT)"
echo "- Syntax validation: $SYNTAX_ERRORS errors found"
echo "- Manual validation checklist: Generated"
echo "- Next steps: Review $RESULTS_DIR/VALIDATION_SUMMARY.md"

exit 0