import pandas as pd
import io

# Create a comprehensive project timeline with phases, tasks, and deliverables
timeline_data = {
    'Phase': [
        'Phase 1: Foundation & Planning', 'Phase 1: Foundation & Planning', 'Phase 1: Foundation & Planning', 'Phase 1: Foundation & Planning',
        'Phase 2: Database Design & Setup', 'Phase 2: Database Design & Setup', 'Phase 2: Database Design & Setup', 'Phase 2: Database Design & Setup',
        'Phase 3: ETL Development', 'Phase 3: ETL Development', 'Phase 3: ETL Development', 'Phase 3: ETL Development',
        'Phase 4: Data Integration & Testing', 'Phase 4: Data Integration & Testing', 'Phase 4: Data Integration & Testing', 'Phase 4: Data Integration & Testing',
        'Phase 5: Analytics & Reporting', 'Phase 5: Analytics & Reporting', 'Phase 5: Analytics & Reporting', 'Phase 5: Analytics & Reporting',
        'Phase 6: Deployment & Optimization', 'Phase 6: Deployment & Optimization', 'Phase 6: Deployment & Optimization', 'Phase 6: Deployment & Optimization'
    ],
    'Task': [
        'Requirements Analysis & Documentation', 'Data Source Inventory & Mapping', 'Technical Architecture Design', 'Project Setup & Environment',
        'Database Schema Implementation', 'Reference Data Structure Creation', 'Index & Constraint Definition', 'Security & Backup Configuration',
        'Email Scraper Development', 'Data Parser & Validator Creation', 'Transformation Logic Implementation', 'Error Handling & Logging',
        'End-to-End Pipeline Testing', 'Data Quality Validation', 'Historical Data Migration', 'Performance Optimization',
        'COS Calculation Views', 'Business Intelligence Reports', 'Anomaly Detection Rules', 'Dashboard Development',
        'Production Deployment', 'Monitoring & Alerting Setup', 'User Training & Documentation', 'Go-Live Support'
    ],
    'Duration_Days': [5, 3, 4, 2, 7, 5, 3, 2, 10, 8, 12, 5, 8, 6, 10, 5, 8, 6, 4, 7, 3, 4, 5, 3],
    'Resources_Required': [
        'Project Manager, Business Analyst', 'Data Analyst, Business Analyst', 'Database Architect, Technical Lead', 'DevOps Engineer, Developer',
        'Database Developer, DBA', 'Database Developer, Data Analyst', 'Database Developer, Performance Analyst', 'DBA, Security Engineer',
        'Python Developer, Email Systems Expert', 'Python Developer, Data Engineer', 'Python Developer, Business Analyst', 'Python Developer, QA Engineer',
        'QA Engineer, Data Engineer', 'Data Analyst, QA Engineer', 'Database Developer, Data Engineer', 'Performance Engineer, DBA',
        'Business Analyst, SQL Developer', 'BI Developer, Report Designer', 'Data Scientist, Business Analyst', 'Frontend Developer, UX Designer',
        'DevOps Engineer, System Administrator', 'DevOps Engineer, Monitoring Specialist', 'Trainer, Technical Writer', 'Support Team, Project Manager'
    ],
    'Key_Deliverables': [
        'Requirements Document, Data Flow Diagrams', 'Data Source Catalog, Field Mapping', 'Technical Architecture, Database Design', 'Development Environment, Git Repository',
        'Physical Database Schema, Tables Created', 'Reference Data Loaded, Relationships Defined', 'Optimized Indexes, Data Constraints', 'Backup Strategy, Security Policies',
        'Automated Email Processing, File Detection', 'Data Parsing Engine, Validation Rules', 'Business Logic, Calculation Engine', 'Error Recovery, Audit Logging',
        'Tested ETL Pipeline, Integration Tests', 'Data Quality Reports, Validation Results', 'Historical Data Loaded, Migration Scripts', 'Performance Tuned Pipeline',
        'COS Analysis Views, Calculation Logic', 'Standard Reports, Executive Dashboard', 'Exception Reports, Alert Rules', 'Interactive Dashboards, Self-Service Tools',
        'Production System, Deployment Scripts', 'Monitoring Dashboard, Alert System', 'User Manuals, Training Materials', 'Stable Production System'
    ],
    'Success_Criteria': [
        'Approved requirements, Clear scope definition', 'Complete data inventory, Mapped relationships', 'Scalable architecture, Technical approval', 'Working development environment',
        'Normalized schema, Performance optimized', 'Clean reference data, Validated relationships', 'Query optimization, Data integrity', 'Secure system, Reliable backups',
        'Reliable file processing, Error handling', 'Accurate data parsing, Quality validation', 'Correct calculations, Business rules', 'Robust error recovery, Full audit trail',
        'End-to-end functionality, Quality assurance', 'Data accuracy validation, Quality metrics', 'Complete historical data, Migration success', 'Performance benchmarks met',
        'Accurate COS calculations, Business validation', 'Actionable insights, User acceptance', 'Proactive issue detection, Alert reliability', 'User-friendly interface, Self-service capability',
        'Stable production system, Performance monitoring', 'Proactive monitoring, Issue prevention', 'Trained users, Complete documentation', 'Business value realization'
    ]
}

timeline_df = pd.DataFrame(timeline_data)

# Calculate cumulative timeline
timeline_df['Start_Day'] = timeline_df['Duration_Days'].cumsum() - timeline_df['Duration_Days'] + 1
timeline_df['End_Day'] = timeline_df['Duration_Days'].cumsum()

# Add week calculations
timeline_df['Start_Week'] = ((timeline_df['Start_Day'] - 1) // 7) + 1
timeline_df['End_Week'] = ((timeline_df['End_Day'] - 1) // 7) + 1

print("VIDA STOCK MOVEMENT ANALYSIS PROJECT - IMPLEMENTATION TIMELINE")
print("=" * 80)

current_phase = ""
phase_total = 0
phase_start = 0

for idx, row in timeline_df.iterrows():
    if row['Phase'] != current_phase:
        if current_phase != "":
            print(f"\n📊 {current_phase} Total Duration: {phase_total} days (Weeks {phase_start}-{((phase_start + phase_total - 2) // 7) + 1})")
            print("-" * 80)
        
        current_phase = row['Phase']
        phase_total = 0
        if idx == 0:
            phase_start = 1
        else:
            phase_start = timeline_df.iloc[idx-1]['End_Day'] + 1
        
        print(f"\n🎯 {current_phase}")
        print("-" * 80)
    
    phase_total += row['Duration_Days']
    
    print(f"\n📋 Task: {row['Task']}")
    print(f"   ⏱️  Duration: {row['Duration_Days']} days (Days {row['Start_Day']}-{row['End_Day']}, Week {row['Start_Week']}-{row['End_Week']})")
    print(f"   👥 Resources: {row['Resources_Required']}")
    print(f"   📦 Deliverables: {row['Key_Deliverables']}")
    print(f"   ✅ Success Criteria: {row['Success_Criteria']}")

# Print final phase total
print(f"\n📊 {current_phase} Total Duration: {phase_total} days (Weeks {phase_start}-{((phase_start + phase_total - 2) // 7) + 1})")
print("-" * 80)

total_days = timeline_df['Duration_Days'].sum()
total_weeks = (total_days - 1) // 7 + 1

print(f"\n🎯 PROJECT SUMMARY")
print("=" * 80)
print(f"Total Duration: {total_days} days ({total_weeks} weeks)")
print(f"Total Phases: 6")
print(f"Total Tasks: {len(timeline_df)}")

# Save to CSV
csv_output = timeline_df.to_csv(index=False)
with open('vida_project_timeline.csv', 'w') as f:
    f.write(csv_output)

print(f"\n📁 Timeline exported to: vida_project_timeline.csv")