from flask import Flask, request
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Load and train model
df = pd.read_csv('house_prices.csv')
X = df[['area', 'bedrooms', 'bathrooms', 'age_of_house', 'distance_to_city_center']]
y = df['price']
model = LinearRegression()
model.fit(X, y)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_html = ""
    if request.method == 'POST':
        try:
            area = float(request.form['area'])
            bedrooms = int(request.form['bedrooms'])
            bathrooms = int(request.form['bathrooms'])
            age = int(request.form['age_of_house'])
            distance = float(request.form['distance_to_city_center'])

            input_df = pd.DataFrame([{
                'area': area,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'age_of_house': age,
                'distance_to_city_center': distance
            }])

            predicted_price = model.predict(input_df)[0]
            prediction_html = f"<div class='result'>🏷 Estimated Price: ₹{int(predicted_price):,}</div>"
        except Exception as e:
            prediction_html = f"<div class='error'>⚠️ Error: {e}</div>"

    # Return the full HTML as response
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>House Price Predictor</title>
      <style>
        body {{
          font-family: 'Segoe UI', sans-serif;
          background-color: #eef2f3;
          margin: 0;
          padding: 40px 0;
        }}
        .container {{
          background-color: white;
          max-width: 500px;
          margin: auto;
          padding: 30px;
          border-radius: 10px;
          box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        h1 {{
          text-align: center;
          color: #2d3436;
          margin-bottom: 20px;
        }}
        form label {{
          display: block;
          margin-top: 15px;
          font-weight: bold;
        }}
        form input {{
          width: 100%;
          padding: 10px;
          margin-top: 5px;
          border-radius: 5px;
          border: 1px solid #bdc3c7;
        }}
        button {{
          margin-top: 25px;
          padding: 12px;
          width: 100%;
          background-color: #0984e3;
          color: white;
          border: none;
          font-size: 16px;
          border-radius: 6px;
          cursor: pointer;
        }}
        button:hover {{
          background-color: #74b9ff;
        }}
        .result {{
          margin-top: 30px;
          text-align: center;
          font-size: 20px;
          color: #2d3436;
        }}
        .error {{
          margin-top: 30px;
          text-align: center;
          font-size: 18px;
          color: red;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>🏠 House Price Predictor</h1>
        <form method="post">
          <label for="area">Area (sqft):</label>
          <input type="number" name="area" step="0.01" required>

          <label for="bedrooms">Number of Bedrooms:</label>
          <input type="number" name="bedrooms" required>

          <label for="bathrooms">Number of Bathrooms:</label>
          <input type="number" name="bathrooms" required>

          <label for="age_of_house">Age of House (years):</label>
          <input type="number" name="age_of_house" required>

          <label for="distance_to_city_center">Distance to City Center (km):</label>
          <input type="number" name="distance_to_city_center" step="0.01" required>

          <button type="submit">Predict Price</button>
        </form>
        {prediction_html}
      </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)