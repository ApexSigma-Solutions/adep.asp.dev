# POML Templates for Task Orchestration

This directory contains comprehensive POML (Process Orchestration Markup Language) templates designed for structured task orchestration across the ApexSigma ecosystem.

## Template Overview

### Core Templates

1. **`sprint_task_orchestration.poml`**
   - **Purpose**: Master template for sprint planning and task management
   - **Use Cases**: Sprint initialization, task delegation, progress tracking
   - **Key Features**: Task categorization (Critical/High/Stretch), agent assignments, dependency management, success metrics

2. **`agent_delegation.poml`**
   - **Purpose**: Structured task delegation to specialized AI agents
   - **Use Cases**: Task assignment, agent coordination, workload balancing
   - **Key Features**: Agent expertise matching, deliverable specification, coordination rules, quality gates

3. **`critical_path_analysis.poml`**
   - **Purpose**: Critical path analysis and bottleneck identification
   - **Use Cases**: Sprint planning, risk assessment, schedule optimization
   - **Key Features**: Dependency analysis, bottleneck resolution, parallel opportunities, contingency planning

4. **`progress_tracking.poml`**
   - **Purpose**: Comprehensive progress monitoring and reporting
   - **Use Cases**: Daily standups, sprint reviews, stakeholder reporting
   - **Key Features**: Task progress, agent performance, integration status, forecasting

## Usage Patterns

### Sprint Planning Workflow
1. Use `sprint_task_orchestration.poml` to structure sprint objectives and tasks
2. Apply `critical_path_analysis.poml` to identify bottlenecks and optimize scheduling
3. Implement `agent_delegation.poml` for structured task assignment
4. Monitor progress using `progress_tracking.poml`

### Integration with ApexSigma Ecosystem
These templates are designed to work with:
- **DevEnviro.as**: Society of Agents orchestration
- **InGest-LLM.as**: Documentation and task ingestion
- **memOS.as**: Knowledge persistence and retrieval
- **tools.as**: Tool discovery and coordination

## Template Features

### Templating Engine Support
- **Jinja2 Syntax**: Variables, loops, conditionals
- **YAML Frontmatter**: Metadata and configuration
- **XML Structure**: Hierarchical data organization
- **JSON Compatibility**: Easy data binding from ecosystem services

### Agent Integration
Each template supports the 12 ApexSigma specialist agents:
- `backend-specialist`, `frontend-specialist`, `devops-engineer`
- `qa-engineer`, `security-engineer`, `software-architect`
- `product-owner`, `project-manager`, `engineering-manager`
- `enterprise-cto`, `technical-writer`, `senior-fullstack-developer`

### Data Binding Examples

```yaml
# Example data structure for sprint_task_orchestration.poml
sprint_context:
  sprint_id: "phase_2_cognitive_expansion"
  sprint_name: "Phase 2: Cognitive Expansion Sprint Plan"
  objectives:
    - "Harden ecosystem reliability"
    - "Expand Agent Society with Sigma Coder integration"

critical_tasks:
  - taskId: "P2-CRIT-01"
    project: "InGest-LLM.as"
    assignedAgent: "Gemini CLI"
    description: "Create dedicated integration test suite"
    dependencies: []
    
agent_assignments:
  "Claude Code":
    role: "Documentation Specialist"
    taskCount: 3
    focusAreas: ["API Documentation", "Bug Tracking", "Knowledge Base"]
```

## Quality Assurance

### Template Validation
- **Schema Validation**: Each template includes metadata for validation
- **Version Control**: Semantic versioning for template evolution
- **Dependency Tracking**: Inter-template relationships documented

### Best Practices
1. **Atomic Templates**: Each template serves a specific orchestration purpose
2. **Composable Design**: Templates can be combined for complex workflows
3. **Context Preservation**: Rich metadata for knowledge persistence
4. **Agent-Agnostic**: Works with any agent in the ApexSigma ecosystem

## Integration with Phase 2 Sprint

These templates directly support the Phase 2 Cognitive Expansion Sprint objectives:
- **Reliability**: Structured task management ensures systematic execution
- **Agent Society**: Native support for all 12 specialist agents
- **Technical Debt**: Built-in tracking for technical debt resolution
- **Observability**: Comprehensive progress tracking and reporting

## Future Enhancements

### Planned Features
- **Real-time Data Binding**: Integration with memOS.as for live data
- **AI-Generated Content**: Dynamic template population from ecosystem state
- **Visual Rendering**: Dashboard generation from template data
- **Automated Orchestration**: Self-updating templates based on progress

### Extension Points
- **Custom Agent Types**: Template support for new agent specializations
- **Domain-Specific Templates**: Templates for specific project types
- **Integration Templates**: Service-to-service coordination patterns
- **Compliance Templates**: Audit trails and compliance reporting

---

**Version**: 2.0  
**Created**: 2025-08-24  
**Last Updated**: 2025-08-24  
**Author**: Claude Code (ApexSigma Ecosystem)  
**Sprint**: Phase 2 Cognitive Expansion