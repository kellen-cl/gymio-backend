# Create this file: gymio_project/views.py

from django.http import HttpResponse
from django.template import Template, Context

def api_home(request):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gymio API - Documentation</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 60px 40px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 3rem;
                margin-bottom: 10px;
                font-weight: 700;
            }
            
            .header p {
                font-size: 1.2rem;
                opacity: 0.9;
            }
            
            .status {
                display: inline-block;
                background: #10b981;
                padding: 8px 20px;
                border-radius: 20px;
                margin-top: 20px;
                font-weight: 600;
            }
            
            .status::before {
                content: "●";
                margin-right: 8px;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            .content {
                padding: 40px;
            }
            
            .section {
                margin-bottom: 40px;
            }
            
            .section h2 {
                color: #667eea;
                font-size: 1.8rem;
                margin-bottom: 20px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }
            
            .endpoints-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            .endpoint-card {
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .endpoint-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.2);
                border-color: #667eea;
            }
            
            .endpoint-card h3 {
                color: #667eea;
                margin-bottom: 10px;
                font-size: 1.2rem;
            }
            
            .endpoint-card .method {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 5px;
                font-size: 0.8rem;
                font-weight: 600;
                margin-bottom: 10px;
            }
            
            .method.get { background: #10b981; color: white; }
            .method.post { background: #3b82f6; color: white; }
            .method.put { background: #f59e0b; color: white; }
            .method.delete { background: #ef4444; color: white; }
            
            .endpoint-url {
                background: #1f2937;
                color: #10b981;
                padding: 10px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 0.9rem;
                margin: 10px 0;
                overflow-x: auto;
            }
            
            .description {
                color: #6b7280;
                font-size: 0.9rem;
                line-height: 1.5;
            }
            
            .quick-links {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                margin-top: 20px;
            }
            
            .btn {
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            
            .btn-secondary {
                background: white;
                color: #667eea;
                border: 2px solid #667eea;
            }
            
            .footer {
                background: #f8f9fa;
                padding: 30px;
                text-align: center;
                color: #6b7280;
            }
            
            .tech-stack {
                display: flex;
                justify-content: center;
                gap: 20px;
                flex-wrap: wrap;
                margin-top: 20px;
            }
            
            .tech-badge {
                background: white;
                padding: 8px 20px;
                border-radius: 20px;
                font-weight: 600;
                color: #667eea;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            @media (max-width: 768px) {
                .header h1 {
                    font-size: 2rem;
                }
                
                .endpoints-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏋️ Gymio API</h1>
                <p>Complete Gym Management System Backend</p>
                <div class="status">API is Running</div>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>📚 Quick Links</h2>
                    <div class="quick-links">
                        <a href="/admin/" class="btn">Admin Dashboard</a>
                        <a href="/api/memberships/plans/" class="btn-secondary btn">Browse API</a>
                    </div>
                </div>
                
                <div class="section">
                    <h2>🔐 Authentication Endpoints</h2>
                    <div class="endpoints-grid">
                        <div class="endpoint-card" onclick="window.location.href='/api/auth/register/'">
                            <span class="method post">POST</span>
                            <h3>Register User</h3>
                            <div class="endpoint-url">/api/auth/register/</div>
                            <p class="description">Create a new user account (member, trainer, or admin)</p>
                        </div>
                        
                        <div class="endpoint-card" onclick="window.location.href='/api/auth/login/'">
                            <span class="method post">POST</span>
                            <h3>Login</h3>
                            <div class="endpoint-url">/api/auth/login/</div>
                            <p class="description">Authenticate user and receive JWT tokens</p>
                        </div>
                        
                        <div class="endpoint-card" onclick="window.location.href='/api/auth/profile/'">
                            <span class="method get">GET</span>
                            <h3>Get Profile</h3>
                            <div class="endpoint-url">/api/auth/profile/</div>
                            <p class="description">Retrieve current user profile information</p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>💳 Membership Endpoints</h2>
                    <div class="endpoints-grid">
                        <div class="endpoint-card" onclick="window.location.href='/api/memberships/plans/'">
                            <span class="method get">GET</span>
                            <h3>Membership Plans</h3>
                            <div class="endpoint-url">/api/memberships/plans/</div>
                            <p class="description">List all available membership plans and pricing</p>
                        </div>
                        
                        <div class="endpoint-card" onclick="window.location.href='/api/memberships/subscriptions/'">
                            <span class="method get">GET</span>
                            <h3>Subscriptions</h3>
                            <div class="endpoint-url">/api/memberships/subscriptions/</div>
                            <p class="description">View and manage user subscriptions</p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>🏋️ Classes & Bookings</h2>
                    <div class="endpoints-grid">
                        <div class="endpoint-card" onclick="window.location.href='/api/classes/'">
                            <span class="method get">GET</span>
                            <h3>Gym Classes</h3>
                            <div class="endpoint-url">/api/classes/</div>
                            <p class="description">Browse all available gym classes and schedules</p>
                        </div>
                        
                        <div class="endpoint-card" onclick="window.location.href='/api/classes/schedule/'">
                            <span class="method get">GET</span>
                            <h3>Weekly Schedule</h3>
                            <div class="endpoint-url">/api/classes/schedule/</div>
                            <p class="description">View full weekly class schedule</p>
                        </div>
                        
                        <div class="endpoint-card" onclick="window.location.href='/api/bookings/'">
                            <span class="method get">GET</span>
                            <h3>My Bookings</h3>
                            <div class="endpoint-url">/api/bookings/</div>
                            <p class="description">View and manage your class bookings</p>
                        </div>
                        
                        <div class="endpoint-card">
                            <span class="method post">POST</span>
                            <h3>Book a Class</h3>
                            <div class="endpoint-url">/api/bookings/</div>
                            <p class="description">Book a spot in a gym class</p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>💰 Payment Endpoints</h2>
                    <div class="endpoints-grid">
                        <div class="endpoint-card" onclick="window.location.href='/api/payments/'">
                            <span class="method get">GET</span>
                            <h3>Payment History</h3>
                            <div class="endpoint-url">/api/payments/</div>
                            <p class="description">View payment history and invoices</p>
                        </div>
                        
                        <div class="endpoint-card" onclick="window.location.href='/api/payments/stats/'">
                            <span class="method get">GET</span>
                            <h3>Payment Statistics</h3>
                            <div class="endpoint-url">/api/payments/stats/</div>
                            <p class="description">Revenue analytics and payment stats (Admin)</p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📝 Content Endpoints</h2>
                    <div class="endpoints-grid">
                        <div class="endpoint-card" onclick="window.location.href='/api/blog/posts/'">
                            <span class="method get">GET</span>
                            <h3>Blog Posts</h3>
                            <div class="endpoint-url">/api/blog/posts/</div>
                            <p class="description">Browse fitness tips and blog articles</p>
                        </div>
                        
                        <div class="endpoint-card" onclick="window.location.href='/api/services/'">
                            <span class="method get">GET</span>
                            <h3>Services</h3>
                            <div class="endpoint-url">/api/services/</div>
                            <p class="description">View gym services and facilities</p>
                        </div>
                        
                        <div class="endpoint-card" onclick="window.location.href='/api/faqs/'">
                            <span class="method get">GET</span>
                            <h3>FAQs</h3>
                            <div class="endpoint-url">/api/faqs/</div>
                            <p class="description">Frequently asked questions</p>
                        </div>
                        
                        <div class="endpoint-card">
                            <span class="method post">POST</span>
                            <h3>Contact Form</h3>
                            <div class="endpoint-url">/api/contact/messages/</div>
                            <p class="description">Submit contact form messages</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <h3 style="color: #667eea; margin-bottom: 15px;">⚡ Built With</h3>
                <div class="tech-stack">
                    <span class="tech-badge">Django 5.0</span>
                    <span class="tech-badge">Django REST Framework</span>
                    <span class="tech-badge">PostgreSQL</span>
                    <span class="tech-badge">JWT Auth</span>
                </div>
                <p style="margin-top: 20px;">© 2025 Gymio. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(html_template)