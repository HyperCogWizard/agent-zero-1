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
