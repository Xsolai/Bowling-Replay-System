import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os
from jinja2 import Template

class EmailService:
    """Handle email sending operations"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "your-email@gmail.com")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "your-app-password")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@bowlingreplay.com")
        self.from_name = os.getenv("FROM_NAME", "Bowling Replay System")
        
        # Base URL for the application
        self.base_url = os.getenv("BASE_URL", "http://localhost:3000")
    
    def send_email(self, to_email: str, subject: str, html_content: str, text_content: Optional[str] = None) -> bool:
        """
        Send an email
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            text_content: Plain text content (optional)
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email
            
            # Create plain text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, "plain")
                message.attach(text_part)
            
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(message)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_verification_email(self, to_email: str, name: str, verification_token: str) -> bool:
        """
        Send email verification email
        
        Args:
            to_email: User email address
            name: User name
            verification_token: Email verification token
            
        Returns:
            True if email was sent successfully
        """
        verification_url = f"{self.base_url}/verify-email?token={verification_token}"
        
        subject = "Verify your email - Bowling Replay System"
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Email Verification</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background-color: #2c3e50; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background-color: #f9f9f9; }
                .button { display: inline-block; padding: 12px 30px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                .footer { padding: 20px; text-align: center; color: #666; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎳 Bowling Replay System</h1>
                </div>
                <div class="content">
                    <h2>Welcome, {{ name }}!</h2>
                    <p>Thank you for signing up for Bowling Replay System. Please verify your email address to complete your registration.</p>
                    <p>Click the button below to verify your email:</p>
                    <a href="{{ verification_url }}" class="button">Verify Email Address</a>
                    <p>If the button doesn't work, copy and paste this link into your browser:</p>
                    <p><a href="{{ verification_url }}">{{ verification_url }}</a></p>
                    <p>This link will expire in 24 hours.</p>
                    <p>If you didn't create an account, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>This email was sent by Bowling Replay System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to Bowling Replay System!
        
        Hi {name},
        
        Thank you for signing up. Please verify your email address by clicking the link below:
        
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create an account, please ignore this email.
        
        Best regards,
        Bowling Replay System Team
        """
        
        template = Template(html_template)
        html_content = template.render(name=name, verification_url=verification_url)
        
        return self.send_email(to_email, subject, html_content, text_content)
    
    def send_password_reset_email(self, to_email: str, name: str, reset_token: str) -> bool:
        """
        Send password reset email
        
        Args:
            to_email: User email address
            name: User name
            reset_token: Password reset token
            
        Returns:
            True if email was sent successfully
        """
        reset_url = f"{self.base_url}/reset-password?token={reset_token}"
        
        subject = "Reset your password - Bowling Replay System"
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Password Reset</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background-color: #2c3e50; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background-color: #f9f9f9; }
                .button { display: inline-block; padding: 12px 30px; background-color: #e74c3c; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                .footer { padding: 20px; text-align: center; color: #666; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎳 Bowling Replay System</h1>
                </div>
                <div class="content">
                    <h2>Password Reset Request</h2>
                    <p>Hi {{ name }},</p>
                    <p>We received a request to reset your password. Click the button below to reset your password:</p>
                    <a href="{{ reset_url }}" class="button">Reset Password</a>
                    <p>If the button doesn't work, copy and paste this link into your browser:</p>
                    <p><a href="{{ reset_url }}">{{ reset_url }}</a></p>
                    <p>This link will expire in 1 hour.</p>
                    <p>If you didn't request a password reset, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>This email was sent by Bowling Replay System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Password Reset Request
        
        Hi {name},
        
        We received a request to reset your password. Click the link below to reset your password:
        
        {reset_url}
        
        This link will expire in 1 hour.
        
        If you didn't request a password reset, please ignore this email.
        
        Best regards,
        Bowling Replay System Team
        """
        
        template = Template(html_template)
        html_content = template.render(name=name, reset_url=reset_url)
        
        return self.send_email(to_email, subject, html_content, text_content)
    
    def send_welcome_email(self, to_email: str, name: str) -> bool:
        """
        Send welcome email after successful verification
        
        Args:
            to_email: User email address
            name: User name
            
        Returns:
            True if email was sent successfully
        """
        subject = "Welcome to Bowling Replay System!"
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Welcome</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background-color: #27ae60; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background-color: #f9f9f9; }
                .button { display: inline-block; padding: 12px 30px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                .footer { padding: 20px; text-align: center; color: #666; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎳 Welcome to Bowling Replay System!</h1>
                </div>
                <div class="content">
                    <h2>Your account is now active!</h2>
                    <p>Hi {{ name }},</p>
                    <p>Congratulations! Your email has been verified and your account is now active.</p>
                    <p>You can now:</p>
                    <ul>
                        <li>🎳 Record your bowling sessions</li>
                        <li>📹 Get AI-powered highlight clips</li>
                        <li>📱 Receive clips via SMS</li>
                        <li>💳 Purchase and share your best moments</li>
                    </ul>
                    <p>Get started by visiting our app:</p>
                    <a href="{{ base_url }}" class="button">Open Bowling Replay App</a>
                    <p>Thank you for choosing Bowling Replay System!</p>
                </div>
                <div class="footer">
                    <p>This email was sent by Bowling Replay System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Welcome to Bowling Replay System!
        
        Hi {name},
        
        Congratulations! Your email has been verified and your account is now active.
        
        You can now:
        - Record your bowling sessions
        - Get AI-powered highlight clips
        - Receive clips via SMS
        - Purchase and share your best moments
        
        Get started by visiting: {self.base_url}
        
        Thank you for choosing Bowling Replay System!
        
        Best regards,
        Bowling Replay System Team
        """
        
        template = Template(html_template)
        html_content = template.render(name=name, base_url=self.base_url)
        
        return self.send_email(to_email, subject, html_content, text_content) 