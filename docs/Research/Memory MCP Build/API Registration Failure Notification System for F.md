<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# API Registration Failure Notification System for FastMCP

A comprehensive notification system for API registration failures ensures quick response to issues and maintains system reliability. Here's a complete implementation with multiple notification channels and escalation policies.

## Core Notification Framework

### Multi-Channel Notification System

```python
import asyncio
import logging
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import smtplib
from email.message import EmailMessage
import httpx
import json

class NotificationLevel(Enum):
    INFO = "info"
    WARNING = "warning" 
    CRITICAL = "critical"
    URGENT = "urgent"

@dataclass
class RegistrationFailure:
    api_name: str
    error_message: str
    timestamp: datetime = field(default_factory=datetime.now)
    failure_type: str = "registration_error"
    retry_count: int = 0
    last_success: Optional[datetime] = None
    impact_level: NotificationLevel = NotificationLevel.WARNING

class APIRegistrationNotificationSystem:
    def __init__(self):
        self.notification_channels = {}
        self.escalation_rules = []
        self.failure_history: List[RegistrationFailure] = []
        self.logger = logging.getLogger(__name__)
        
    def add_notification_channel(self, name: str, handler: Callable):
        """Add a notification channel (email, slack, webhook, etc.)"""
        self.notification_channels[name] = handler
        self.logger.info(f"Added notification channel: {name}")
    
    def add_escalation_rule(self, condition: Callable, action: Callable, delay_minutes: int = 0):
        """Add escalation rule based on failure conditions"""
        self.escalation_rules.append({
            'condition': condition,
            'action': action,
            'delay_minutes': delay_minutes,
            'last_triggered': None
        })
    
    async def notify_failure(self, failure: RegistrationFailure):
        """Process and notify about a registration failure"""
        self.failure_history.append(failure)
        
        # Determine notification level based on failure context
        failure.impact_level = self._assess_impact_level(failure)
        
        # Send immediate notifications
        await self._send_notifications(failure)
        
        # Check escalation rules
        await self._check_escalations()
        
        # Clean up old failures (keep last 100)
        if len(self.failure_history) > 100:
            self.failure_history = self.failure_history[-100:]
    
    def _assess_impact_level(self, failure: RegistrationFailure) -> NotificationLevel:
        """Assess the impact level of the failure"""
        
        # Check for repeated failures of the same API
        recent_failures = [f for f in self.failure_history 
                          if f.api_name == failure.api_name 
                          and f.timestamp > datetime.now() - timedelta(hours=1)]
        
        if len(recent_failures) >= 3:
            return NotificationLevel.CRITICAL
        
        # Check for critical API failures
        critical_apis = ['payments', 'authentication', 'core_services']
        if failure.api_name.lower() in critical_apis:
            return NotificationLevel.URGENT
        
        # Check for widespread failures
        total_recent_failures = len([f for f in self.failure_history 
                                   if f.timestamp > datetime.now() - timedelta(minutes=15)])
        
        if total_recent_failures >= 5:
            return NotificationLevel.CRITICAL
        
        return NotificationLevel.WARNING
    
    async def _send_notifications(self, failure: RegistrationFailure):
        """Send notifications through all configured channels"""
        
        notification_data = {
            'api_name': failure.api_name,
            'error_message': failure.error_message,
            'timestamp': failure.timestamp.isoformat(),
            'impact_level': failure.impact_level.value,
            'retry_count': failure.retry_count,
            'failure_context': self._generate_failure_context()
        }
        
        # Send through each channel based on impact level
        for channel_name, handler in self.notification_channels.items():
            try:
                should_send = self._should_send_to_channel(channel_name, failure.impact_level)
                if should_send:
                    await handler(notification_data)
                    self.logger.info(f"Sent notification via {channel_name}")
            except Exception as e:
                self.logger.error(f"Failed to send notification via {channel_name}: {e}")
    
    def _should_send_to_channel(self, channel_name: str, impact_level: NotificationLevel) -> bool:
        """Determine if notification should be sent to specific channel based on impact"""
        
        channel_rules = {
            'email': [NotificationLevel.WARNING, NotificationLevel.CRITICAL, NotificationLevel.URGENT],
            'slack': [NotificationLevel.CRITICAL, NotificationLevel.URGENT],
            'sms': [NotificationLevel.URGENT],
            'webhook': [NotificationLevel.WARNING, NotificationLevel.CRITICAL, NotificationLevel.URGENT],
            'pagerduty': [NotificationLevel.CRITICAL, NotificationLevel.URGENT]
        }
        
        return impact_level in channel_rules.get(channel_name, [impact_level])
    
    async def _check_escalations(self):
        """Check and trigger escalation rules"""
        
        for rule in self.escalation_rules:
            try:
                # Check if rule condition is met
                if rule['condition'](self.failure_history):
                    # Check if enough time has passed since last trigger
                    now = datetime.now()
                    if (rule['last_triggered'] is None or 
                        now > rule['last_triggered'] + timedelta(minutes=rule['delay_minutes'])):
                        
                        await rule['action'](self.failure_history)
                        rule['last_triggered'] = now
                        
            except Exception as e:
                self.logger.error(f"Escalation rule failed: {e}")
    
    def _generate_failure_context(self) -> Dict[str, Any]:
        """Generate context information about recent failures"""
        
        now = datetime.now()
        last_hour_failures = [f for f in self.failure_history 
                            if f.timestamp > now - timedelta(hours=1)]
        
        api_failure_counts = {}
        for failure in last_hour_failures:
            api_failure_counts[failure.api_name] = api_failure_counts.get(failure.api_name, 0) + 1
        
        return {
            'total_failures_last_hour': len(last_hour_failures),
            'failed_apis': list(api_failure_counts.keys()),
            'api_failure_counts': api_failure_counts,
            'most_problematic_api': max(api_failure_counts.items(), key=lambda x: x[1])[0] if api_failure_counts else None
        }
```


## Notification Channel Implementations

### Email Notification Handler

```python
import smtplib
from email.message import EmailMessage
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

class EmailNotificationHandler:
    def __init__(self, smtp_config: Dict[str, Any]):
        self.smtp_server = smtp_config['server']
        self.smtp_port = smtp_config['port']
        self.username = smtp_config['username'] 
        self.password = smtp_config['password']
        self.from_email = smtp_config['from_email']
        self.to_emails = smtp_config['to_emails']
        self.use_tls = smtp_config.get('use_tls', True)
        
    async def __call__(self, notification_data: Dict[str, Any]):
        """Send email notification"""
        
        subject = self._generate_subject(notification_data)
        body = self._generate_email_body(notification_data)
        
        msg = MimeMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.from_email
        msg['To'] = ", ".join(self.to_emails)
        
        # Add plain text and HTML parts
        text_part = MimeText(body['text'], 'plain')
        html_part = MimeText(body['html'], 'html')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        try:
            if self.use_tls:
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    server.login(self.username, self.password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.username, self.password) 
                    server.send_message(msg)
                    
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")
    
    def _generate_subject(self, data: Dict[str, Any]) -> str:
        impact_emoji = {
            'info': '💡',
            'warning': '⚠️', 
            'critical': '🚨',
            'urgent': '🔥'
        }
        
        emoji = impact_emoji.get(data['impact_level'], '⚠️')
        return f"{emoji} API Registration Failure: {data['api_name']}"
    
    def _generate_email_body(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Generate both text and HTML email body"""
        
        # Text version
        text_body = f"""
API Registration Failure Alert

API Name: {data['api_name']}
Error: {data['error_message']}
Impact Level: {data['impact_level'].upper()}
Timestamp: {data['timestamp']}
Retry Count: {data['retry_count']}

Context Information:
- Total failures in last hour: {data['failure_context']['total_failures_last_hour']}
- Failed APIs: {', '.join(data['failure_context']['failed_apis'])}

Please investigate and resolve this issue promptly.
        """
        
        # HTML version
        impact_colors = {
            'info': '#17a2b8',
            'warning': '#ffc107',
            'critical': '#dc3545', 
            'urgent': '#e83e8c'
        }
        
        color = impact_colors.get(data['impact_level'], '#ffc107')
        
        html_body = f"""
        <html>
          <body>
            <h2 style="color: {color};">API Registration Failure Alert</h2>
            
            <table border="1" style="border-collapse: collapse; width: 100%;">
              <tr>
                <td style="padding: 8px; background-color: #f8f9fa;"><strong>API Name</strong></td>
                <td style="padding: 8px;">{data['api_name']}</td>
              </tr>
              <tr>
                <td style="padding: 8px; background-color: #f8f9fa;"><strong>Error Message</strong></td>
                <td style="padding: 8px;">{data['error_message']}</td>
              </tr>
              <tr>
                <td style="padding: 8px; background-color: #f8f9fa;"><strong>Impact Level</strong></td>
                <td style="padding: 8px; color: {color};"><strong>{data['impact_level'].upper()}</strong></td>
              </tr>
              <tr>
                <td style="padding: 8px; background-color: #f8f9fa;"><strong>Timestamp</strong></td>
                <td style="padding: 8px;">{data['timestamp']}</td>
              </tr>
              <tr>
                <td style="padding: 8px; background-color: #f8f9fa;"><strong>Retry Count</strong></td>
                <td style="padding: 8px;">{data['retry_count']}</td>
              </tr>
            </table>
            
            <h3>Context Information</h3>
            <ul>
              <li>Total failures in last hour: {data['failure_context']['total_failures_last_hour']}</li>
              <li>Failed APIs: {', '.join(data['failure_context']['failed_apis'])}</li>
            </ul>
            
            <p><strong>Please investigate and resolve this issue promptly.</strong></p>
          </body>
        </html>
        """
        
        return {'text': text_body, 'html': html_body}
```


### Slack Notification Handler

```python
class SlackNotificationHandler:
    def __init__(self, webhook_url: str, channel: str = None):
        self.webhook_url = webhook_url
        self.channel = channel
        
    async def __call__(self, notification_data: Dict[str, Any]):
        """Send Slack notification"""
        
        color_map = {
            'info': '#36a64f',
            'warning': '#ffeb3b', 
            'critical': '#f44336',
            'urgent': '#e91e63'
        }
        
        color = color_map.get(notification_data['impact_level'], '#ffeb3b')
        
        slack_payload = {
            'attachments': [{
                'color': color,
                'title': f"API Registration Failure: {notification_data['api_name']}",
                'fields': [
                    {
                        'title': 'Error Message',
                        'value': notification_data['error_message'],
                        'short': False
                    },
                    {
                        'title': 'Impact Level',
                        'value': notification_data['impact_level'].upper(),
                        'short': True
                    },
                    {
                        'title': 'Retry Count', 
                        'value': str(notification_data['retry_count']),
                        'short': True
                    },
                    {
                        'title': 'Recent Failures',
                        'value': f"{notification_data['failure_context']['total_failures_last_hour']} in last hour",
                        'short': True
                    }
                ],
                'timestamp': int(datetime.fromisoformat(notification_data['timestamp'].replace('Z', '+00:00')).timestamp()),
                'footer': 'FastMCP API Monitor'
            }]
        }
        
        if self.channel:
            slack_payload['channel'] = self.channel
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.webhook_url,
                json=slack_payload,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
```


### Webhook Notification Handler

```python
class WebhookNotificationHandler:
    def __init__(self, webhook_url: str, auth_headers: Dict[str, str] = None):
        self.webhook_url = webhook_url
        self.auth_headers = auth_headers or {}
        
    async def __call__(self, notification_data: Dict[str, Any]):
        """Send webhook notification"""
        
        payload = {
            'event_type': 'api_registration_failure',
            'timestamp': notification_data['timestamp'],
            'data': {
                'api_name': notification_data['api_name'],
                'error_message': notification_data['error_message'],
                'impact_level': notification_data['impact_level'],
                'retry_count': notification_data['retry_count'],
                'context': notification_data['failure_context']
            }
        }
        
        headers = {
            'Content-Type': 'application/json',
            **self.auth_headers
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.webhook_url,
                json=payload,
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
```


## Advanced Notification Features

### Smart Notification Throttling

```python
class NotificationThrottler:
    def __init__(self):
        self.notification_counts = {}
        self.throttle_rules = {
            'per_api_per_hour': 3,  # Max 3 notifications per API per hour
            'total_per_hour': 10,   # Max 10 total notifications per hour
            'critical_exempt': True  # Critical notifications bypass throttling
        }
        
    def should_send_notification(self, api_name: str, impact_level: NotificationLevel) -> bool:
        """Check if notification should be sent based on throttling rules"""
        
        # Critical and urgent notifications bypass throttling
        if (impact_level in [NotificationLevel.CRITICAL, NotificationLevel.URGENT] and 
            self.throttle_rules['critical_exempt']):
            return True
            
        now = datetime.now()
        hour_key = now.strftime('%Y-%m-%d-%H')
        
        # Initialize counters if needed
        if hour_key not in self.notification_counts:
            self.notification_counts[hour_key] = {'total': 0, 'per_api': {}}
            
        hour_counts = self.notification_counts[hour_key]
        
        # Check total notifications per hour
        if hour_counts['total'] >= self.throttle_rules['total_per_hour']:
            return False
            
        # Check per-API notifications per hour
        api_count = hour_counts['per_api'].get(api_name, 0)
        if api_count >= self.throttle_rules['per_api_per_hour']:
            return False
            
        # Update counters
        hour_counts['total'] += 1
        hour_counts['per_api'][api_name] = api_count + 1
        
        return True
```


### Escalation Policy System

```python
class EscalationPolicyManager:
    def __init__(self, notification_system: APIRegistrationNotificationSystem):
        self.notification_system = notification_system
        
    def setup_default_escalations(self):
        """Setup default escalation policies"""
        
        # Escalation 1: Multiple failures of same API
        def same_api_failures_condition(failures: List[RegistrationFailure]) -> bool:
            api_failures = {}
            cutoff = datetime.now() - timedelta(minutes=30)
            
            for failure in failures:
                if failure.timestamp > cutoff:
                    api_failures[failure.api_name] = api_failures.get(failure.api_name, 0) + 1
                    
            return any(count >= 3 for count in api_failures.values())
        
        async def escalate_to_team_lead(failures: List[RegistrationFailure]):
            # Send high-priority notification to team leads
            most_failed_api = max(failures, key=lambda f: failures.count(f.api_name)).api_name
            await self._send_escalation_notification(
                'team_leads',
                f"Critical: API '{most_failed_api}' has failed multiple times",
                failures
            )
            
        self.notification_system.add_escalation_rule(
            same_api_failures_condition,
            escalate_to_team_lead,
            delay_minutes=5
        )
        
        # Escalation 2: Widespread failures
        def widespread_failures_condition(failures: List[RegistrationFailure]) -> bool:
            recent_failures = [f for f in failures 
                             if f.timestamp > datetime.now() - timedelta(minutes=15)]
            unique_apis = set(f.api_name for f in recent_failures)
            return len(unique_apis) >= 5
        
        async def escalate_to_management(failures: List[RegistrationFailure]):
            await self._send_escalation_notification(
                'management',
                'URGENT: Widespread API registration failures detected',
                failures
            )
            
        self.notification_system.add_escalation_rule(
            widespread_failures_condition,
            escalate_to_management,
            delay_minutes=2
        )
        
        # Escalation 3: Critical API down for extended period
        def critical_api_down_condition(failures: List[RegistrationFailure]) -> bool:
            critical_apis = ['payments', 'authentication', 'core_services']
            cutoff = datetime.now() - timedelta(minutes=10)
            
            for api in critical_apis:
                api_failures = [f for f in failures 
                              if f.api_name == api and f.timestamp > cutoff]
                if len(api_failures) >= 2:
                    return True
            return False
        
        async def escalate_to_oncall(failures: List[RegistrationFailure]):
            await self._send_escalation_notification(
                'oncall',
                'CRITICAL: Core API service registration failing',
                failures
            )
            
        self.notification_system.add_escalation_rule(
            critical_api_down_condition,
            escalate_to_oncall,
            delay_minutes=0  # Immediate escalation
        )
    
    async def _send_escalation_notification(self, recipient_group: str, 
                                          message: str, 
                                          failures: List[RegistrationFailure]):
        """Send escalation notification to specific recipient group"""
        
        escalation_data = {
            'event_type': 'escalation',
            'recipient_group': recipient_group,
            'message': message,
            'failure_count': len(failures),
            'affected_apis': list(set(f.api_name for f in failures)),
            'timestamp': datetime.now().isoformat()
        }
        
        # Send through high-priority channels
        if recipient_group == 'oncall':
            # Page on-call engineer
            await self.notification_system.notification_channels.get('pagerduty', lambda x: None)(escalation_data)
            await self.notification_system.notification_channels.get('sms', lambda x: None)(escalation_data)
        
        # Always send email for escalations
        await self.notification_system.notification_channels.get('email', lambda x: None)(escalation_data)
```


## Complete Integration Example

```python
async def setup_notification_system():
    """Complete example of setting up the notification system"""
    
    # Initialize the notification system
    notification_system = APIRegistrationNotificationSystem()
    
    # Setup email notifications
    email_config = {
        'server': 'smtp.gmail.com',
        'port': 587,
        'username': 'your-email@gmail.com',
        'password': 'your-app-password',
        'from_email': 'noreply@yourcompany.com',
        'to_emails': ['dev-team@yourcompany.com', 'sre@yourcompany.com'],
        'use_tls': True
    }
    email_handler = EmailNotificationHandler(email_config)
    notification_system.add_notification_channel('email', email_handler)
    
    # Setup Slack notifications
    slack_handler = SlackNotificationHandler(
        webhook_url='https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK',
        channel='#api-alerts'
    )
    notification_system.add_notification_channel('slack', slack_handler)
    
    # Setup webhook notifications
    webhook_handler = WebhookNotificationHandler(
        webhook_url='https://your-monitoring-system.com/webhooks/api-failures',
        auth_headers={'Authorization': 'Bearer YOUR_TOKEN'}
    )
    notification_system.add_notification_channel('webhook', webhook_handler)
    
    # Setup escalation policies
    escalation_manager = EscalationPolicyManager(notification_system)
    escalation_manager.setup_default_escalations()
    
    # Add throttling
    throttler = NotificationThrottler()
    
    return notification_system, throttler

# Usage in FastMCP registration process
async def register_apis_with_notifications():
    """Example of integrating notifications with API registration"""
    
    from fastmcp import FastMCP
    
    # Setup notification system
    notification_system, throttler = await setup_notification_system()
    
    # Initialize FastMCP
    mcp = FastMCP("Production Server")
    
    # API registration configuration
    apis_to_register = [
        {'name': 'users', 'url': 'https://api.users.com'},
        {'name': 'payments', 'url': 'https://api.payments.com'},
        {'name': 'inventory', 'url': 'https://api.inventory.com'}
    ]
    
    # Register each API with failure notifications
    for api_config in apis_to_register:
        try:
            # Attempt API registration (pseudo-code)
            success = await register_single_api(mcp, api_config)
            
            if not success:
                # Create failure record
                failure = RegistrationFailure(
                    api_name=api_config['name'],
                    error_message="Registration failed - see logs for details",
                    failure_type="registration_error"
                )
                
                # Send notification if not throttled
                if throttler.should_send_notification(failure.api_name, failure.impact_level):
                    await notification_system.notify_failure(failure)
                
        except Exception as e:
            # Handle registration exceptions
            failure = RegistrationFailure(
                api_name=api_config['name'],
                error_message=str(e),
                failure_type="registration_exception"
            )
            
            if throttler.should_send_notification(failure.api_name, failure.impact_level):
                await notification_system.notify_failure(failure)

# Run the registration with notifications
if __name__ == "__main__":
    asyncio.run(register_apis_with_notifications())
```

This comprehensive notification system provides:

- **Multi-Channel Support**: Email, Slack, webhooks, SMS, and PagerDuty integration
- **Smart Throttling**: Prevents notification spam while ensuring critical alerts get through
- **Impact Assessment**: Automatically determines failure severity and routes notifications accordingly
- **Escalation Policies**: Automated escalation based on failure patterns and severity
- **Rich Context**: Detailed failure information and system context for faster resolution
- **Flexible Configuration**: Easy to customize for different environments and teams

The system ensures that API registration failures are promptly detected, properly categorized, and communicated to the right people through appropriate channels, enabling quick response and resolution.

