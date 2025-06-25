#!/usr/bin/env python3
"""
Feature Validation System for agent-zero-1
Implements cognitive flowchart for recursive feature validation and adaptive attention allocation
"""

import os
import sys
import json
import subprocess
import importlib.util
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class FeatureStatus(Enum):
    """Status enumeration for features"""
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    ATTENTION_REQUIRED = "attention_required"
    MANUAL_VALIDATION_NEEDED = "manual_validation_needed"


@dataclass
class FeatureNode:
    """Represents a feature node in the hypergraph"""
    name: str
    path: str
    feature_type: str  # 'python_tool', 'api_endpoint', 'web_component', 'core_module'
    dependencies: List[str]
    description: str
    status: FeatureStatus = FeatureStatus.UNKNOWN
    test_results: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        result['status'] = self.status.value
        return result


class FeatureHypergraph:
    """
    Feature hypergraph for managing feature nodes and their relationships
    Implements the cognitive flowchart structure from the issue
    """
    
    def __init__(self):
        self.nodes: Dict[str, FeatureNode] = {}
        self.edges: Dict[str, Set[str]] = {}  # feature_name -> set of dependent features
        
    def add_node(self, node: FeatureNode):
        """Add a feature node to the hypergraph"""
        self.nodes[node.name] = node
        if node.name not in self.edges:
            self.edges[node.name] = set()
            
    def add_dependency(self, from_feature: str, to_feature: str):
        """Add a dependency edge between features"""
        if from_feature not in self.edges:
            self.edges[from_feature] = set()
        self.edges[from_feature].add(to_feature)
        
    def get_dependent_features(self, feature_name: str) -> Set[str]:
        """Get all features that depend on the given feature"""
        dependents = set()
        for node_name, deps in self.edges.items():
            if feature_name in deps:
                dependents.add(node_name)
        return dependents
        
    def propagate_status(self, feature_name: str, status: FeatureStatus):
        """Propagate status changes to dependent features (recursive attention allocation)"""
        if feature_name in self.nodes:
            self.nodes[feature_name].status = status
            
            # If this feature fails, mark dependents for attention
            if status == FeatureStatus.FAIL:
                dependents = self.get_dependent_features(feature_name)
                for dependent in dependents:
                    if self.nodes[dependent].status != FeatureStatus.FAIL:
                        self.nodes[dependent].status = FeatureStatus.ATTENTION_REQUIRED
                        
    def to_dict(self) -> Dict[str, Any]:
        """Convert hypergraph to dictionary for JSON serialization"""
        return {
            'nodes': {name: node.to_dict() for name, node in self.nodes.items()},
            'edges': {name: list(deps) for name, deps in self.edges.items()}
        }


class FeatureEnumerator:
    """
    Feature Enumeration Node - Maps all feature modules
    Extracts capabilities from documentation, codebase, and recent commits
    """
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.hypergraph = FeatureHypergraph()
        
    def enumerate_features(self) -> FeatureHypergraph:
        """
        Main enumeration method - builds the feature hypergraph
        Maps features from Python tools, API endpoints, web components, and core modules
        """
        print("[1] Feature Enumeration Node - Mapping all feature modules...")
        
        # Enumerate Python tools
        self._enumerate_python_tools()
        
        # Enumerate API endpoints
        self._enumerate_api_endpoints()
        
        # Enumerate web components
        self._enumerate_web_components()
        
        # Enumerate core modules
        self._enumerate_core_modules()
        
        # Build dependency relationships
        self._build_dependencies()
        
        print(f"   Found {len(self.hypergraph.nodes)} features in the hypergraph")
        return self.hypergraph
        
    def _enumerate_python_tools(self):
        """Enumerate Python tools from python/tools directory"""
        tools_dir = self.base_path / "python" / "tools"
        if not tools_dir.exists():
            return
            
        for tool_file in tools_dir.glob("*.py"):
            if tool_file.name == "__init__.py":
                continue
                
            tool_name = tool_file.stem
            
            # Extract description from docstring if available
            description = self._extract_python_description(tool_file)
            
            node = FeatureNode(
                name=f"tool_{tool_name}",
                path=str(tool_file.relative_to(self.base_path)),
                feature_type="python_tool",
                dependencies=[],
                description=description
            )
            self.hypergraph.add_node(node)
            
    def _enumerate_api_endpoints(self):
        """Enumerate API endpoints from python/api directory"""
        api_dir = self.base_path / "python" / "api"
        if not api_dir.exists():
            return
            
        for api_file in api_dir.glob("*.py"):
            if api_file.name == "__init__.py":
                continue
                
            endpoint_name = api_file.stem
            
            # Extract description from docstring if available
            description = self._extract_python_description(api_file)
            
            node = FeatureNode(
                name=f"api_{endpoint_name}",
                path=str(api_file.relative_to(self.base_path)),
                feature_type="api_endpoint",
                dependencies=[],
                description=description
            )
            self.hypergraph.add_node(node)
            
    def _enumerate_web_components(self):
        """Enumerate web components from webui directory"""
        webui_dir = self.base_path / "webui"
        if not webui_dir.exists():
            return
            
        # Main web interface
        if (webui_dir / "index.html").exists():
            node = FeatureNode(
                name="web_interface_main",
                path="webui/index.html",
                feature_type="web_component",
                dependencies=[],
                description="Main web interface for agent-zero-1"
            )
            self.hypergraph.add_node(node)
            
        # JavaScript components
        js_dir = webui_dir / "js"
        if js_dir.exists():
            for js_file in js_dir.glob("*.js"):
                component_name = js_file.stem
                
                node = FeatureNode(
                    name=f"web_{component_name}",
                    path=str(js_file.relative_to(self.base_path)),
                    feature_type="web_component",
                    dependencies=[],
                    description=f"Web component: {component_name}"
                )
                self.hypergraph.add_node(node)
                
    def _enumerate_core_modules(self):
        """Enumerate core modules from the root directory"""
        core_files = [
            "agent.py", "initialize.py", "models.py", 
            "run_cli.py", "run_ui.py", "run_tunnel.py"
        ]
        
        for core_file in core_files:
            file_path = self.base_path / core_file
            if file_path.exists():
                module_name = file_path.stem
                description = self._extract_python_description(file_path)
                
                node = FeatureNode(
                    name=f"core_{module_name}",
                    path=core_file,
                    feature_type="core_module",
                    dependencies=[],
                    description=description
                )
                self.hypergraph.add_node(node)
                
    def _extract_python_description(self, file_path: Path) -> str:
        """Extract description from Python file docstring or comments"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for module docstring
            lines = content.split('\n')
            for i, line in enumerate(lines[:20]):  # Check first 20 lines
                stripped = line.strip()
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    # Find closing quote
                    quote_type = '"""' if stripped.startswith('"""') else "'''"
                    docstring_lines = []
                    
                    # If docstring is on same line
                    if stripped.count(quote_type) >= 2:
                        return stripped.replace(quote_type, '').strip()
                    
                    # Multi-line docstring
                    for j in range(i + 1, min(i + 10, len(lines))):
                        if quote_type in lines[j]:
                            break
                        docstring_lines.append(lines[j].strip())
                    
                    return ' '.join(docstring_lines).strip()
                    
            return f"Python module: {file_path.name}"
            
        except Exception as e:
            return f"Python module: {file_path.name} (description extraction failed)"
            
    def _build_dependencies(self):
        """Build dependency relationships between features"""
        # Add some known dependencies based on agent-zero-1 architecture
        
        # Core dependencies
        self.hypergraph.add_dependency("tool_code_execution_tool", "core_initialize")
        self.hypergraph.add_dependency("tool_knowledge_tool", "core_models")
        self.hypergraph.add_dependency("tool_memory_save", "core_agent")
        self.hypergraph.add_dependency("tool_memory_load", "core_agent")
        
        # API dependencies
        for node_name in self.hypergraph.nodes:
            if node_name.startswith("api_"):
                self.hypergraph.add_dependency(node_name, "core_initialize")
                
        # Web component dependencies
        for node_name in self.hypergraph.nodes:
            if node_name.startswith("web_") and node_name != "web_interface_main":
                self.hypergraph.add_dependency(node_name, "web_interface_main")


class EnvironmentValidator:
    """
    Environment Initialization Node - Establishes isolated test environments
    Monitors for missing or version-conflicting packages
    """
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        
    def validate_environment(self) -> Dict[str, Any]:
        """
        Validate the environment setup according to installation.md
        Returns validation results
        """
        print("[2] Environment Initialization Node - Validating setup...")
        
        results = {
            "python_version": self._check_python_version(),
            "requirements": self._check_requirements(),
            "docker_availability": self._check_docker(),
            "file_structure": self._check_file_structure(),
            "status": "unknown"
        }
        
        # Determine overall status
        if all(r.get("status") == "pass" for r in results.values() if isinstance(r, dict)):
            results["status"] = "pass"
        elif any(r.get("status") == "fail" for r in results.values() if isinstance(r, dict)):
            results["status"] = "fail"
        else:
            results["status"] = "attention_required"
            
        return results
        
    def _check_python_version(self) -> Dict[str, Any]:
        """Check Python version compatibility"""
        try:
            version = sys.version_info
            if version >= (3, 8):
                return {"status": "pass", "version": f"{version.major}.{version.minor}.{version.micro}"}
            else:
                return {"status": "fail", "version": f"{version.major}.{version.minor}.{version.micro}", 
                       "error": "Python 3.8+ required"}
        except Exception as e:
            return {"status": "fail", "error": str(e)}
            
    def _check_requirements(self) -> Dict[str, Any]:
        """Check if requirements.txt dependencies are available"""
        requirements_file = self.base_path / "requirements.txt"
        if not requirements_file.exists():
            return {"status": "fail", "error": "requirements.txt not found"}
            
        try:
            with open(requirements_file, 'r') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                
            missing = []
            for req in requirements:
                # Simple package name extraction (before any version specifiers)
                pkg_name = req.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].strip()
                
                try:
                    importlib.import_module(pkg_name)
                except ImportError:
                    missing.append(pkg_name)
                    
            if missing:
                return {
                    "status": "attention_required", 
                    "missing_packages": missing,
                    "total_requirements": len(requirements)
                }
            else:
                return {"status": "pass", "total_requirements": len(requirements)}
                
        except Exception as e:
            return {"status": "fail", "error": str(e)}
            
    def _check_docker(self) -> Dict[str, Any]:
        """Check Docker availability"""
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return {"status": "pass", "version": result.stdout.strip()}
            else:
                return {"status": "attention_required", "error": "Docker not available"}
        except FileNotFoundError:
            return {"status": "attention_required", "error": "Docker not found in PATH"}
        except Exception as e:
            return {"status": "fail", "error": str(e)}
            
    def _check_file_structure(self) -> Dict[str, Any]:
        """Check essential file structure"""
        essential_paths = [
            "agent.py", "initialize.py", "requirements.txt",
            "python/tools", "python/api", "webui", "docs"
        ]
        
        missing = []
        for path in essential_paths:
            if not (self.base_path / path).exists():
                missing.append(path)
                
        if missing:
            return {"status": "fail", "missing_paths": missing}
        else:
            return {"status": "pass", "verified_paths": len(essential_paths)}


class TestHarness:
    """
    Automated Test Harness Node - Discovers existing test suites
    If absent, recursively generates minimal test scaffolds for each feature node
    """
    
    def __init__(self, base_path: str, hypergraph: FeatureHypergraph):
        self.base_path = Path(base_path)
        self.hypergraph = hypergraph
        
    def discover_and_run_tests(self) -> Dict[str, Any]:
        """
        Discover existing test suites and run them
        Generate minimal tests for features lacking coverage
        """
        print("[3] Automated Test Harness Node - Discovering and running tests...")
        
        results = {
            "existing_tests": self._discover_existing_tests(),
            "generated_tests": self._generate_minimal_tests(),
            "test_results": {},
            "coverage_analysis": {}
        }
        
        # Run discovered tests
        results["test_results"] = self._run_available_tests()
        
        # Analyze coverage
        results["coverage_analysis"] = self._analyze_coverage()
        
        return results
        
    def _discover_existing_tests(self) -> Dict[str, Any]:
        """Discover existing test infrastructure"""
        discovered = {
            "pytest_available": self._check_pytest(),
            "test_directories": self._find_test_directories(),
            "test_files": self._find_test_files()
        }
        
        return discovered
        
    def _check_pytest(self) -> bool:
        """Check if pytest is available"""
        try:
            import pytest
            return True
        except ImportError:
            return False
            
    def _find_test_directories(self) -> List[str]:
        """Find test directories"""
        test_dirs = []
        for path in self.base_path.rglob("*"):
            if path.is_dir() and any(test_name in path.name.lower() for test_name in ['test', 'tests']):
                test_dirs.append(str(path.relative_to(self.base_path)))
        return test_dirs
        
    def _find_test_files(self) -> List[str]:
        """Find test files"""
        test_files = []
        for path in self.base_path.rglob("*.py"):
            if any(test_name in path.name.lower() for test_name in ['test_', '_test', 'tests']):
                test_files.append(str(path.relative_to(self.base_path)))
        return test_files
        
    def _generate_minimal_tests(self) -> Dict[str, str]:
        """Generate minimal test scaffolds for features lacking coverage"""
        generated = {}
        
        for feature_name, feature_node in self.hypergraph.nodes.items():
            if feature_node.feature_type == "python_tool":
                test_code = self._generate_tool_test(feature_node)
                generated[feature_name] = test_code
                
        return generated
        
    def _generate_tool_test(self, feature_node: FeatureNode) -> str:
        """Generate a minimal test for a Python tool"""
        tool_name = feature_node.name.replace("tool_", "")
        return f"""
# Minimal test for {feature_node.name}
def test_{tool_name}_import():
    \"\"\"Test that {tool_name} can be imported\"\"\"
    try:
        from python.tools.{tool_name} import *
        return True
    except ImportError as e:
        return False, str(e)

def test_{tool_name}_instantiation():
    \"\"\"Test that {tool_name} can be instantiated\"\"\"
    try:
        from python.tools.{tool_name} import *
        # This is a minimal test - actual implementation would need more specific testing
        return True
    except Exception as e:
        return False, str(e)
"""
        
    def _run_available_tests(self) -> Dict[str, Any]:
        """Run any available tests"""
        results = {}
        
        # Try to run pytest if available
        if self._check_pytest():
            try:
                result = subprocess.run(
                    ['python', '-m', 'pytest', '--tb=short', '-v'],
                    cwd=self.base_path,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                results["pytest"] = {
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            except subprocess.TimeoutExpired:
                results["pytest"] = {"error": "Test execution timed out"}
            except Exception as e:
                results["pytest"] = {"error": str(e)}
        else:
            results["pytest"] = {"status": "not_available"}
            
        return results
        
    def _analyze_coverage(self) -> Dict[str, Any]:
        """Analyze test coverage for features"""
        coverage = {}
        
        for feature_name, feature_node in self.hypergraph.nodes.items():
            # Simple coverage analysis based on existing tests
            has_specific_test = any(
                feature_name.replace("tool_", "").replace("api_", "").replace("web_", "") in test_file
                for test_file in self._find_test_files()
            )
            
            coverage[feature_name] = {
                "has_specific_test": has_specific_test,
                "needs_manual_validation": not has_specific_test
            }
            
        return coverage


def main():
    """Main entry point for feature validation system"""
    base_path = Path(__file__).parent
    
    print("Agent Zero Feature Validation System")
    print("=" * 50)
    
    # Initialize components
    enumerator = FeatureEnumerator(str(base_path))
    env_validator = EnvironmentValidator(str(base_path))
    
    # Run validation pipeline
    try:
        # 1. Feature Enumeration
        hypergraph = enumerator.enumerate_features()
        
        # 2. Environment Validation
        env_results = env_validator.validate_environment()
        
        # 3. Test Harness
        test_harness = TestHarness(str(base_path), hypergraph)
        test_results = test_harness.discover_and_run_tests()
        
        # 4. Generate report
        report = {
            "timestamp": str(subprocess.check_output(['date'], text=True).strip()),
            "feature_hypergraph": hypergraph.to_dict(),
            "environment_validation": env_results,
            "test_results": test_results,
            "summary": {
                "total_features": len(hypergraph.nodes),
                "environment_status": env_results["status"],
                "features_needing_attention": len([
                    n for n in hypergraph.nodes.values() 
                    if n.status in [FeatureStatus.FAIL, FeatureStatus.ATTENTION_REQUIRED]
                ])
            }
        }
        
        # Save report
        report_file = base_path / "feature_validation_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n[✓] Feature validation complete! Report saved to: {report_file}")
        print(f"    Total features discovered: {report['summary']['total_features']}")
        print(f"    Environment status: {report['summary']['environment_status']}")
        print(f"    Features needing attention: {report['summary']['features_needing_attention']}")
        
        return 0
        
    except Exception as e:
        print(f"\n[✗] Feature validation failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())