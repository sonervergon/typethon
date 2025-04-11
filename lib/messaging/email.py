import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional, Dict, Any
from fastapi import Depends
from pathlib import Path
import jinja2

from core.config import (
    SMTP_SERVER, 
    SMTP_PORT, 
    SMTP_USERNAME, 
    SMTP_PASSWORD, 
    EMAIL_FROM_ADDRESS,
    EMAIL_TEMPLATES_DIR
)

class EmailService:
    def __init__(self):
        self.server = SMTP_SERVER
        self.port = SMTP_PORT
        self.username = SMTP_USERNAME
        self.password = SMTP_PASSWORD
        self.from_email = EMAIL_FROM_ADDRESS
        
        # Template environment
        template_dir = Path(EMAIL_TEMPLATES_DIR)
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
    
    def _get_connection(self):
        """Get SMTP connection"""
        connection = smtplib.SMTP(self.server, self.port)
        connection.starttls()
        if self.username and self.password:
            connection.login(self.username, self.password)
        return connection
    
    def send_email(
        self, 
        to_email: List[str], 
        subject: str, 
        body: str, 
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        is_html: bool = False
    ) -> bool:
        """Send a simple email"""
        if not to_email:
            return False
            
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = ', '.join(to_email)
        msg['Subject'] = subject
        
        if cc:
            msg['Cc'] = ', '.join(cc)
        if bcc:
            msg['Bcc'] = ', '.join(bcc)
            
        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
        
        try:
            with self._get_connection() as server:
                all_recipients = to_email + (cc or []) + (bcc or [])
                server.send_message(msg, self.from_email, all_recipients)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def send_template_email(
        self,
        to_email: List[str],
        subject: str,
        template_name: str,
        template_vars: Dict[str, Any],
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """Send an email using a template"""
        try:
            template = self.template_env.get_template(template_name)
            html_content = template.render(**template_vars)
            return self.send_email(to_email, subject, html_content, cc, bcc, is_html=True)
        except Exception as e:
            print(f"Failed to render or send template email: {e}")
            return False

# Singleton instance
_email_service = None

def get_email_service() -> EmailService:
    """Dependency to get Email service instance"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service 