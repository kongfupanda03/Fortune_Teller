"""Email sending service for verification and password reset"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Email configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
APP_URL = os.getenv("APP_URL", "http://localhost:3000")


def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Send an email"""
    
    if not SMTP_USER or not SMTP_PASSWORD:
        print("⚠️  Email not configured. Check SMTP settings in .env")
        print(f"📧 Would send email to {to_email}: {subject}")
        return False
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = FROM_EMAIL
        message["To"] = to_email
        
        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {str(e)}")
        return False


def send_verification_email(to_email: str, username: str, token: str) -> bool:
    """Send email verification link"""
    
    verification_url = f"{APP_URL}/verify-email?token={token}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; padding: 15px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✨ Welcome to Constellation Fortune Teller ✨</h1>
            </div>
            <div class="content">
                <h2>Hello, {username}!</h2>
                <p>Thank you for joining us on this cosmic journey. We're thrilled to have you!</p>
                <p>To complete your registration and unlock the mysteries of the stars, please verify your email address by clicking the button below:</p>
                <p style="text-align: center;">
                    <a href="{verification_url}" class="button">Verify My Email</a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background: white; padding: 10px; border-radius: 5px;">{verification_url}</p>
                <p><strong>This link will expire in 24 hours.</strong></p>
                <p>If you didn't create an account with us, please ignore this email.</p>
                <p>May the stars guide your path! 🔮</p>
            </div>
            <div class="footer">
                <p>© 2025 Constellation Fortune Teller | Your Cosmic Destiny Awaits</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(to_email, "✨ Verify Your Email - Constellation Fortune Teller", html_content)


def send_password_reset_email(to_email: str, username: str, token: str) -> bool:
    """Send password reset link"""
    
    reset_url = f"{APP_URL}/reset-password?token={token}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; padding: 15px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔮 Password Reset Request</h1>
            </div>
            <div class="content">
                <h2>Hello, {username}!</h2>
                <p>We received a request to reset your password for your Constellation Fortune Teller account.</p>
                <p>Click the button below to create a new password:</p>
                <p style="text-align: center;">
                    <a href="{reset_url}" class="button">Reset My Password</a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; background: white; padding: 10px; border-radius: 5px;">{reset_url}</p>
                <div class="warning">
                    <strong>⚠️ Security Notice:</strong>
                    <ul>
                        <li>This link will expire in 1 hour</li>
                        <li>If you didn't request this reset, please ignore this email</li>
                        <li>Your password will remain unchanged unless you click the link</li>
                    </ul>
                </div>
                <p>If you're having trouble, please contact our support.</p>
                <p>Stay safe and may the cosmos protect you! ✨</p>
            </div>
            <div class="footer">
                <p>© 2025 Constellation Fortune Teller | Secure & Mystical</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(to_email, "🔑 Reset Your Password - Constellation Fortune Teller", html_content)

