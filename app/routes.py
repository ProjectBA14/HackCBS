from flask import jsonify, render_template, session, redirect, url_for, request
from auth.auth_config import auth0, requires_auth, mock_requires_auth
import random

def configure_routes(app):
    @app.route('/')
    def dashboard():
        # Simulate random data for demonstration
        if 'user' in session:
            random_data = {
                'portfolio_value': f"${random.randint(5000, 20000)}",
                'monthly_return': f"+{random.uniform(1, 10):.2f}%",
                'yearly_return': f"+{random.uniform(10, 30):.2f}%",
            }
            return render_template('dashboard.html', user=session['user'], data=random_data)
        else:
            return redirect(url_for('/'))

    @app.route('/portfolio')
    @mock_requires_auth
    def portfolio():
        return render_template('portfolio.html')



    @app.route('/reports')
    @mock_requires_auth
    def reports():
        if 'user' in session:
            # Generate random data for bar and pie charts
            bar_chart_data = {
                'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
                'values': [random.randint(1000, 5000) for _ in range(7)]
            }
            pie_chart_data = {
                'labels': ['Bitcoin', 'Ethereum', 'Ripple', 'Litecoin', 'Cardano'],
                'values': [random.randint(5, 30) for _ in range(5)]
            }
            return render_template('reports.html', user=session['user'], bar_chart_data=bar_chart_data, pie_chart_data=pie_chart_data)
        else:
            return redirect(url_for(''))

    @app.route('/profile')
    @mock_requires_auth
    def profile():
        if 'user' in session:
            return render_template('profile.html', user=session['user'])
        else:
            return redirect(url_for(''))
    
    @app.route('/login')
    def login():
        # Faking user data
        fake_user = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'sub': 'auth0|1234567890'  # You can simulate the Auth0 user ID here

        }

        # Store the fake user in session
        session['user'] = fake_user

        # Redirect to the dashboard (or wherever you need to go after login)
        return redirect(url_for('dashboard'))



    @app.route('/callback')
    def callback():
        # Instead of using auth0 to get user info, mock the user info
        userinfo = {'sub': 'mock_user', 'name': 'Test User', 'email': 'test@example.com'}
        session['user'] = userinfo
        return render_template('callback.html', user=userinfo)

        # Sample data generation for e-commerce trends
    def generate_trend_data():
        ecommerce_sites = ["Amazon", "eBay", "Walmart", "Shopify", "Alibaba"]
        trends = []
        for site in ecommerce_sites:
            trend = {
                "site": site,
                "sales_growth": round(random.uniform(1, 20), 2),
                "popular_products": random.choices(
                    ["Laptops", "Smartphones", "Headphones", "Clothing", "Shoes", "Books"], k=3
                ),
                "customer_sentiment": random.choice(["Positive", "Neutral", "Negative"]),
                "region_interest": random.choice(["North America", "Europe", "Asia", "South America", "Africa"]),
            }
            trends.append(trend)
        return trends

    # Route for market trends page
    @app.route('/market-trends')
    def market_trends():
        return render_template('market_trends.html')

    # Route to serve the generated market trend data
    @app.route('/api/trends')
    def get_trends():
        trends = generate_trend_data()
        return jsonify(trends)

    # Route to handle Q&A about trends
    @app.route('/api/ask', methods=['POST'])
    def ask_question():
        question = request.json.get('question')
        # Simple rule-based responses for demo purposes
        if "growth" in question.lower():
            response = "Sales growth varies by platform, with Amazon showing the highest growth this month."
        elif "popular" in question.lower():
            response = "Popular products include Laptops and Smartphones."
        elif "sentiment" in question.lower():
            response = "Customer sentiment is generally positive for Amazon and neutral for eBay."
        else:
            response = "I'm here to help! Try asking about growth, popular products, or customer sentiment."

        return jsonify({"response": response})
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('https://your-auth0-domain.auth0.com/v2/logout?returnTo=http://localhost:8001&client_id=1I1UFlfiBrhZgJa7xnnrev3XDRiaqpUN')
