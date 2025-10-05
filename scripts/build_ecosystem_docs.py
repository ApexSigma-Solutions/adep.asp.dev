#!/usr/bin/env python3
"""
Unified Build Script for ApexSigma Ecosystem Documentation

This script implements the MkDocs instruction across all ApexSigma projects,
providing a unified documentation build process following the three-part strategy:
1. Source of Truth (/.md/ & Code Docstrings)
2. Agent Ingestion (/.ingest/)  
3. Public Docs (/docs/)
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Dict


class ApexSigmaDocsBuilder:
    """Unified documentation builder for the ApexSigma ecosystem."""
    
    def __init__(self, workspace_path: str):
        """Initialize the builder with workspace path."""
        self.workspace = Path(workspace_path)
        self.projects = [
            "devenviro.as",
            "InGest-LLM.as", 
            "memos.as",
            "tools.as",
            "embedding-agent.as"
        ]
        
    def get_project_path(self, project_name: str) -> Path:
        """Get the full path to a project."""
        return self.workspace / project_name
        
    def has_mkdocs(self, project_path: Path) -> bool:
        """Check if project has mkdocs.yml configuration."""
        return (project_path / "mkdocs.yml").exists()
        
    def install_docs_dependencies(self, project_path: Path) -> bool:
        """Install documentation dependencies for a project."""
        print(f"📦 Installing docs dependencies for {project_path.name}")
        
        # Check for Poetry project
        if (project_path / "pyproject.toml").exists():
            try:
                result = subprocess.run(
                    ["poetry", "install", "--with", "docs"],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f"✅ Poetry docs dependencies installed for {project_path.name}")
                    return True
                else:
                    print(f"⚠️ Poetry install failed for {project_path.name}: {result.stderr}")
            except FileNotFoundError:
                print(f"⚠️ Poetry not found for {project_path.name}")
                
        # Check for pip requirements
        if (project_path / "requirements.txt").exists() or (project_path / "requirements-docker.txt").exists():
            req_file = "requirements.txt" if (project_path / "requirements.txt").exists() else "requirements-docker.txt"
            try:
                result = subprocess.run(
                    ["pip", "install", "-r", req_file],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f"✅ Pip dependencies installed for {project_path.name}")
                    return True
                else:
                    print(f"⚠️ Pip install failed for {project_path.name}: {result.stderr}")
            except FileNotFoundError:
                print(f"⚠️ Pip not found for {project_path.name}")
                
        return False
        
    def build_project_docs(self, project_path: Path) -> bool:
        """Build documentation for a single project."""
        if not self.has_mkdocs(project_path):
            print(f"⏭️  Skipping {project_path.name} - no mkdocs.yml found")
            return False
            
        print(f"🏗️  Building docs for {project_path.name}")
        
        try:
            # Build the documentation
            result = subprocess.run(
                ["mkdocs", "build", "--clean"],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ Documentation built successfully for {project_path.name}")
                site_path = project_path / "site"
                if site_path.exists():
                    print(f"📁 Site generated at: {site_path}")
                return True
            else:
                print(f"❌ Build failed for {project_path.name}:")
                print(f"   Error: {result.stderr}")
                print(f"   Output: {result.stdout}")
                return False
                
        except FileNotFoundError:
            print(f"❌ MkDocs not found for {project_path.name}. Please install with 'pip install mkdocs mkdocs-material mkdocstrings[python]'")
            return False
            
    def serve_project_docs(self, project_name: str, port: int = 8000) -> None:
        """Serve documentation for a specific project."""
        project_path = self.get_project_path(project_name)
        
        if not self.has_mkdocs(project_path):
            print(f"❌ No mkdocs.yml found for {project_name}")
            return
            
        print(f"🚀 Serving docs for {project_name} on http://localhost:{port}")
        
        try:
            subprocess.run(
                ["mkdocs", "serve", "--dev-addr", f"localhost:{port}"],
                cwd=project_path
            )
        except FileNotFoundError:
            print(f"❌ MkDocs not found. Please install with 'pip install mkdocs mkdocs-material mkdocstrings[python]'")
        except KeyboardInterrupt:
            print(f"\n📴 Documentation server stopped for {project_name}")
            
    def build_all_docs(self) -> Dict[str, bool]:
        """Build documentation for all projects."""
        print("🚀 Building ApexSigma Ecosystem Documentation")
        print("=" * 50)
        
        results = {}
        
        for project_name in self.projects:
            project_path = self.get_project_path(project_name)
            
            if not project_path.exists():
                print(f"⚠️  Project {project_name} not found at {project_path}")
                results[project_name] = False
                continue
                
            print(f"\n📖 Processing {project_name}")
            print("-" * 30)
            
            # Install dependencies
            self.install_docs_dependencies(project_path)
            
            # Build documentation
            success = self.build_project_docs(project_path)
            results[project_name] = success
            
        return results
        
    def generate_summary(self, results: Dict[str, bool]) -> None:
        """Generate a summary of the build results."""
        print("\n" + "=" * 50)
        print("📊 BUILD SUMMARY")
        print("=" * 50)
        
        successful = [name for name, success in results.items() if success]
        failed = [name for name, success in results.items() if not success]
        
        print(f"✅ Successful builds: {len(successful)}")
        for name in successful:
            print(f"   - {name}")
            
        if failed:
            print(f"\n❌ Failed builds: {len(failed)}")
            for name in failed:
                print(f"   - {name}")
                
        print(f"\n📈 Overall success rate: {len(successful)}/{len(results)} ({len(successful)/len(results)*100:.1f}%)")
        
        if successful:
            print("\n🌐 Access documentation:")
            for name in successful:
                project_path = self.get_project_path(name)
                site_path = project_path / "site" / "index.html"
                if site_path.exists():
                    print(f"   - {name}: file://{site_path.absolute()}")


def main():
    """Main entry point for the documentation builder."""
    if len(sys.argv) < 2:
        print("Usage: python build_ecosystem_docs.py <command> [project_name] [port]")
        print("Commands:")
        print("  build         - Build documentation for all projects")
        print("  serve <name>  - Serve documentation for a specific project")
        print("  list          - List available projects")
        sys.exit(1)
        
    workspace_path = Path(__file__).parent
    builder = ApexSigmaDocsBuilder(str(workspace_path))
    
    command = sys.argv[1]
    
    if command == "build":
        results = builder.build_all_docs()
        builder.generate_summary(results)
        
    elif command == "serve":
        if len(sys.argv) < 3:
            print("❌ Please specify a project name to serve")
            print(f"Available projects: {', '.join(builder.projects)}")
            sys.exit(1)
            
        project_name = sys.argv[2]
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8000
        
        if project_name not in builder.projects:
            print(f"❌ Unknown project: {project_name}")
            print(f"Available projects: {', '.join(builder.projects)}")
            sys.exit(1)
            
        builder.serve_project_docs(project_name, port)
        
    elif command == "list":
        print("📋 Available ApexSigma projects:")
        for project in builder.projects:
            project_path = builder.get_project_path(project)
            status = "✅" if builder.has_mkdocs(project_path) else "⚠️"
            print(f"   {status} {project}")
            
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()