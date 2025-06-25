# Agent Zero Feature Validation System

This directory contains a comprehensive feature validation system for agent-zero-1, implementing the cognitive flowchart approach for recursive implementation pathways and adaptive attention allocation as specified in the requirements.

## 🧠 Cognitive Flowchart Implementation

The validation system implements all 8 nodes of the cognitive flowchart:

1. **Feature Enumeration Node** - Maps all feature modules and builds hypergraph
2. **Environment Initialization Node** - Establishes and validates test environments  
3. **Automated Test Harness Node** - Discovers/creates test scaffolds
4. **Manual Validation Pathway** - Provides structured manual test protocols
5. **Emergent Pattern Detection Node** - Analyzes outputs for anomalies
6. **Recursive Debug/Refine Cycle** - Traces failures along hypergraph edges
7. **Meta-Validation Node** - System-level and neural-symbolic pathway validation
8. **Documentation & Reporting Node** - Updates hypergraph and generates reports

## 📁 System Components

### Core Validation Engine
- **`feature_validation.py`** - Main Python validation system
  - `FeatureHypergraph` class for managing feature relationships
  - `FeatureEnumerator` for discovering all system components
  - `EnvironmentValidator` for setup verification  
  - `TestHarness` for test discovery and execution

### Test Execution Scripts
- **`test_all.sh`** - Complete validation with dependency installation
- **`test_all_demo.sh`** - Demo mode without external dependencies
- **`cognitive_validation.scm`** - Scheme implementation for recursive validation

### Generated Outputs
- **`feature_validation_report.json`** - Comprehensive hypergraph and results
- **`test_results/`** - Timestamped validation runs with detailed reports

## 🚀 Quick Start

### Option 1: Demo Mode (No Dependencies)
```bash
# Run validation without installing external packages
./test_all_demo.sh
```

### Option 2: Full Validation
```bash
# Run complete validation with dependency installation
./test_all.sh
```

### Option 3: Python Only
```bash
# Run just the feature enumeration and analysis
python3 feature_validation.py
```

### Option 4: Scheme Cognitive System
```bash
# Run the recursive cognitive validation (requires Scheme interpreter)
guile cognitive_validation.scm
# or
racket cognitive_validation.scm
```

## 📊 Feature Hypergraph Structure

The system automatically discovers and maps:

- **Python Tools** (19 discovered): Code execution, memory, knowledge, browser, etc.
- **API Endpoints** (33 discovered): Message handling, scheduling, settings, etc.
- **Web Components** (12 discovered): Settings, chat, scheduler interfaces
- **Core Modules** (6 discovered): Agent, initialization, models, runners

### Hypergraph Relationships
```
Core Modules → Tools → API Endpoints → Web Components
     ↓             ↓         ↓            ↓
Dependencies flow and attention allocation paths
```

## 🔍 Validation Results

### Discovered Components
- **Total Features**: 71 mapped in hypergraph
- **Python Syntax**: All files validated
- **Environment Status**: Attention required (dependencies)
- **Test Coverage**: Minimal (manual validation needed)

### Key Findings
1. **No existing automated test infrastructure** - System relies on manual validation
2. **All Python syntax valid** - No compilation errors detected
3. **Complete file structure** - All essential components present
4. **Dependency management needed** - External packages required for full functionality

## 📋 Manual Validation Checklist

### Core Functionality
- [ ] Agent initialization: `python3 run_cli.py` or `python3 run_ui.py`
- [ ] Tool system: Code execution, memory operations, knowledge retrieval
- [ ] Web interface: Settings, chat, scheduler functionality
- [ ] API endpoints: Message handling, authentication, error responses

### Integration Testing
- [ ] Agent-to-agent communication and delegation
- [ ] Tool integration with cognitive modules
- [ ] Memory persistence and retrieval
- [ ] Knowledge base access and search

### UI/UX Validation
- [ ] Web interface loads without errors
- [ ] Interactive components respond correctly
- [ ] Settings panel functional
- [ ] Real-time streaming works

## 🔄 Recursive Debug/Refine Protocol

### For Each Failure Node:

1. **Trace Back**: Follow hypergraph dependency edges to source
2. **Identify Root Cause**: Determine if cascading failure or isolated issue
3. **Apply Fix**: Make minimal targeted changes
4. **Rerun Affected**: Test fix and all dependent features
5. **Update Hypergraph**: Document status changes

### Adaptive Attention Allocation:
- **High Priority**: Core modules (agent.py, initialize.py)
- **Medium Priority**: Tools and API endpoints  
- **Low Priority**: UI components and documentation

## 📈 Pattern Detection

The system analyzes test results for:
- **High failure rates** (>20%) indicating systemic issues
- **Low test coverage** (>50% manual) suggesting automation gaps
- **Dependency cascades** where single failures affect multiple features
- **Integration bottlenecks** in the hypergraph structure

## 🛠️ Extensibility

### Adding New Feature Types
```python
# In feature_validation.py
def _enumerate_custom_features(self):
    """Add custom feature discovery logic"""
    # Your enumeration code here
```

### Custom Validation Rules
```python
# Add to TestHarness class
def _validate_custom_feature(self, feature_node):
    """Custom validation logic"""
    # Your validation code here
```

### Scheme Integration
```scheme
;; In cognitive_validation.scm
(define (custom-test-feature feature-node)
  "Custom recursive test logic"
  ;; Your Scheme validation code here)
```

## 📝 Report Structure

### Generated Files
```
test_results/validation_TIMESTAMP/
├── VALIDATION_SUMMARY.md          # Executive summary
├── feature_validation_report.json # Complete hypergraph data
├── structure_analysis.txt         # Component breakdown
├── manual_validation_checklist.md # Human verification tasks
├── pattern_analysis.md            # Emergent pattern findings
├── debug_refine_protocol.md       # Recursive debugging guide
├── meta_validation.log            # System integrity check
└── *.log                          # Execution logs
```

## 🔧 Configuration

### Environment Variables
The system respects standard agent-zero-1 configuration:
- `.env` files for API keys and settings
- `requirements.txt` for Python dependencies
- Docker configuration if available

### Validation Settings
```python
# Customize in feature_validation.py
FEATURE_TYPES = ["python_tool", "api_endpoint", "web_component", "core_module"]
DEPENDENCY_PATTERNS = {...}  # Known dependency relationships
ATTENTION_PRIORITIES = {...}  # Adaptive attention allocation weights
```

## 🎯 Next Steps

1. **Install Dependencies**: Set up complete Python environment
2. **Run Full Validation**: Execute `./test_all.sh` for comprehensive testing
3. **Complete Manual Tests**: Use generated checklists for human verification
4. **Address Issues**: Focus on features marked "ATTENTION_REQUIRED"
5. **Implement Automation**: Add automated tests for high-priority components
6. **Update Hypergraph**: Document findings and maintain feature relationships

## 🔬 Advanced Usage

### Hypergraph Analysis
```python
# Load and analyze the feature hypergraph
import json
with open('feature_validation_report.json') as f:
    data = json.load(f)
    
# Access specific features
nodes = data['feature_hypergraph']['nodes']
edges = data['feature_hypergraph']['edges']

# Find critical paths
critical_features = [name for name, node in nodes.items() 
                    if node['feature_type'] == 'core_module']
```

### Custom Test Integration
```bash
# Add your own test scripts
mkdir -p tests/custom
echo "#!/bin/bash\n# Your custom test" > tests/custom/my_test.sh
chmod +x tests/custom/my_test.sh

# The validation system will discover and report on custom tests
```

## 📚 References

- **Issue Specification**: Feature Validation in agent-zero-1 - Recursive Implementation Pathways & Adaptive Attention Allocation
- **Architecture Documentation**: `docs/architecture.md`
- **Installation Guide**: `docs/installation.md`
- **Agent Zero Repository**: Core framework documentation

---

**Cognitive Flowchart Complete**: The feature validation system provides comprehensive recursive pathways for validating agent-zero-1 functionality with adaptive attention allocation across the feature hypergraph.