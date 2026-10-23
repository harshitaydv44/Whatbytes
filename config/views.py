from django.http import HttpResponse


def home(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Healthcare Management System</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                color: #1e293b;
                background: #fff;
            }
            * {
                box-sizing: border-box;
            }
            header {
                padding: 24px;
                color: #ffdf5b;
                background: #417f94;
                text-align: center;
            }
            header p {
                color: white;
            }
            main {
                width: min(1200px, 100%);
                margin: 32px auto;
                padding: 0 24px;
            }
            .hero, .card {
                padding: 24px;
                border-radius: 4px;
                background: white;
                box-shadow: 0 2px 8px #0f172a14;
            }
            .status {
                color: #417f94;
                font-weight: bold;
            }
            .card {
                border-top: 5px solid #417f94;
            }
            .card h3 {
                color: #417f94;
            }
            .cards {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                align-items: stretch;
                gap: 16px;
                margin-top: 20px;
            }
            .card {
                min-width: 0;
            }
            .card h3 {
                line-height: 1.35;
            }
            .endpoint {
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                gap: 8px 12px;
                padding: 12px 0;
                border-bottom: 1px solid #e2e8f0;
            }
            .endpoint:last-child {
                border-bottom: 0;
            }
            .method {
                flex: 0 0 auto;
                color: #417f94;
                font-weight: bold;
            }
            .endpoint code {
                display: block;
                max-width: 100%;
                overflow-wrap: anywhere;
            }
            .endpoint-detail {
                display: block;
            }
            .endpoint-detail .method {
                display: block;
                margin-bottom: 6px;
            }
            a {
                display: inline-block;
                color: white;
                text-decoration: none;
                padding: 10px 15px;
                border-radius: 3px;
                font-size: 14px;
                background: #417f94;
            }
            a:hover {
                color: #1e293b;
                background: #ffdf5b;
            }
            footer {
                text-align: center;
                color: #64748b;
                padding: 25px;
            }
            @media (max-width: 1050px) {
                .cards {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }
            }
            @media (max-width: 600px) {
                header {
                    padding: 20px 16px;
                }
                header h1 {
                    font-size: 1.6rem;
                }
                main {
                    margin: 20px auto;
                    padding: 0 16px;
                }
                .hero, .card {
                    padding: 18px;
                }
                .cards {
                    grid-template-columns: 1fr;
                    gap: 14px;
                }
                footer {
                    padding: 20px 16px;
                }
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Healthcare Management System</h1>
            <p>Backend API Dashboard</p>
        </header>
        <main>
            <section class="hero">
                <span class="status">&#10003; Backend server is running</span>
                <h2>Welcome to the Healthcare API</h2>
                <p>
                    Use the API links below in order. Authenticated endpoints
                    require login. For browser testing, log in with your
                    account first.
                </p>
                <a href="/api-auth/login/">Log in to use the API</a>
            </section>
            <section class="cards">
                <div class="card">
                    <h3>1. Authentication</h3>
                    <div class="endpoint">
                        <span class="method">POST</span>
                        <a href="/api/auth/register/">Register</a>
                    </div>
                    <div class="endpoint">
                        <span class="method">POST</span>
                        <a href="/api/auth/login/">Log in</a>
                    </div>
                </div>
                <div class="card">
                    <h3>2. Patient Management</h3>
                    <div class="endpoint">
                        <span class="method">POST</span>
                        <a href="/api/patients/">Create patient</a>
                    </div>
                    <div class="endpoint">
                        <span class="method">GET</span>
                        <a href="/api/patients/">List my patients</a>
                    </div>
                    <div class="endpoint">
                        <div class="endpoint-detail">
                            <span class="method">GET / PUT / DELETE</span>
                            <code>/api/patients/&lt;id&gt;/</code>
                        </div>
                    </div>
                </div>
                <div class="card">
                    <h3>3. Doctor Management</h3>
                    <div class="endpoint">
                        <span class="method">POST</span>
                        <a href="/api/doctors/">Create doctor</a>
                    </div>
                    <div class="endpoint">
                        <span class="method">GET</span>
                        <a href="/api/doctors/">List doctors</a>
                    </div>
                    <div class="endpoint">
                        <div class="endpoint-detail">
                            <span class="method">GET / PUT / DELETE</span>
                            <code>/api/doctors/&lt;id&gt;/</code>
                        </div>
                    </div>
                </div>
                <div class="card">
                    <h3>4. Patient-Doctor Mappings</h3>
                    <div class="endpoint">
                        <span class="method">POST</span>
                        <a href="/api/mappings/">Assign doctor</a>
                    </div>
                    <div class="endpoint">
                        <span class="method">GET</span>
                        <a href="/api/mappings/">List mappings</a>
                    </div>
                    <div class="endpoint">
                        <span class="method">GET</span>
                        <code>/api/mappings/&lt;patient_id&gt;/</code>
                    </div>
                    <div class="endpoint">
                        <span class="method">DELETE</span>
                        <code>/api/mappings/&lt;id&gt;/</code>
                    </div>
                </div>
                <div class="card">
                    <h3>Administration</h3>
                    <p>Manage application data through Django Admin.</p>
                    <a href="/admin/">Open Admin Panel</a>
                </div>
            </section>
        </main>
        <footer>
            Healthcare Management System &copy; 2026
        </footer>
    </body>
    </html>
    """
    return HttpResponse(html)
