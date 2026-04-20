# Stock Market Prediction System

## Project Overview

This project is a Machine Learning-based Stock Market Prediction System developed to analyze stock price movement and generate prediction-based insights for investors.

The system predicts:

- Future closing price of a stock using Linear Regression
- Buy / Hold / Sell signals using Logistic Regression

The project uses real-time stock market data fetched through yFinance and applies feature engineering techniques to improve prediction accuracy and model performance.

---

## Why I Built This Project

During college, I had a minor subject related to the Stock Market, which made me deeply interested in understanding how stock analysis and prediction work.

Instead of only studying theory, I wanted to build something practical that could apply both stock market concepts and machine learning together.

That is when I decided to create a Stock Market Prediction System that could perform technical analysis and prediction using real market data.

This project helped me combine:

- Stock market knowledge
- Machine learning fundamentals
- Data analysis
- API integration
- Model deployment

into one real-world project.

---

## Learning Process

Since I was still a beginner in Machine Learning, I consulted my seniors for guidance. They suggested starting with simple and strong foundational models like:

- Linear Regression
- Logistic Regression

instead of directly using complex deep learning models.

I first learned:

### Linear Regression

Used for predicting continuous values.

In this project, it helps predict the next closing price of a stock.

Example:
If today's closing price is ₹2500, the model predicts whether tomorrow it may become ₹2525 or ₹2470.

---

### Logistic Regression

Used for classification problems.

In this project, it helps generate trading signals like:

- Buy
- Hold
- Sell

based on stock behavior and market indicators.

---

To understand the full machine learning workflow, I learned from:

- Krish Naik’s YouTube channel (Machine Learning project structure)
- Zerodha Varsity / Zerodha educational stock market playlists
- Additional YouTube resources on feature engineering and stock prediction

These resources helped me understand:

- Feature Engineering
- Moving Averages
- Lag Features
- Accuracy Score
- R² Score
- MAE (Mean Absolute Error)
- Model evaluation techniques
- Real-world ML project building

---

## Problem Statement

Initially, I started the project using only one feature:

- Closing Price

because my college teacher advised focusing mainly on closing price analysis since it is one of the most important indicators in stock prediction.

Although opening price and other features can be included, closing price is considered the strongest base for prediction.

---

## Initial Model Performance

At first, I trained the model using only the closing price.

The results were poor:

- Accuracy: around 30–40%
- R² Score: negative value

This clearly showed that using only one feature was not enough for real stock market prediction.

This became one of the biggest learning points of the project.

---

## Feature Engineering Improvements

After analyzing the poor performance, I understood that proper Feature Engineering was necessary.

I then added multiple technical indicators such as:

- Moving Average (MA)
- Exponential Moving Average (EMA)
- Return Percentage
- Lag Features
- High-Low Spread
- Open-Close Spread
- Candle Body Percentage
- Volume Change Percentage
- Trend Strength
- Previous Day Closing Prices
- Previous Returns

These features helped the model understand actual market behavior better instead of relying only on raw closing price.

This significantly improved model performance.

---

## Final Model Performance

After applying proper feature engineering:

- Accuracy improved to around 70%
- R² Score improved to 0.8+

This was a major improvement and showed that feature engineering is often more important than simply choosing a complex model.

Since stock markets are highly dynamic and affected by many unpredictable external factors like news, politics, global events, and investor sentiment, achieving perfect prediction is unrealistic.

That is why achieving stable performance with a strong R² score was considered a successful outcome.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- yFinance
- FastAPI
- Render (Deployment)
- Machine Learning
- Feature Engineering
- Stock Market Technical Analysis

---

## Challenges Faced

During this project, I faced several real-world challenges:

### 1. Poor Initial Accuracy

Using only closing price resulted in poor prediction accuracy and negative R² score.

This taught me the importance of proper feature engineering.

---

### 2. Understanding Technical Indicators

Learning stock market indicators like Moving Averages, Lag Features, EMA, and trend analysis required significant research and understanding.

This was challenging because both finance knowledge and ML understanding were needed together.

---

### 3. Deployment Issues

Deploying the FastAPI project on Render created dependency issues, API failures, and uptime problems.

To solve this, I added:

- `/health` endpoint
- self-ping logic

to keep the deployed API active.

---

### 4. Stock Symbol Issues

Some stocks like BAJAJ.NS created ticker mismatch problems with yFinance.

Handling NSE ticker formats correctly was another practical issue during development.

---

## Key Learnings

This project taught me that:

- Real-world Machine Learning is mostly about data cleaning and feature engineering
- Simple models can perform very well if features are strong
- Deployment is often harder than model training
- Building production-ready ML systems requires API monitoring and maintenance
- Stock market prediction is never perfect because markets are highly unpredictable

---

## Future Improvements

In future versions, I plan to add:

- LSTM / Deep Learning models
- Sentiment Analysis using financial news
- Live dashboard visualization
- Multi-stock comparison system
- Risk analysis module
- Portfolio recommendation system

---

## Author

Aryan Rawat

Aspiring Data Scientist | Machine Learning Enthusiast | Stock Market Learner

This project reflects both my academic learning and practical implementation journey in Machine Learning and Financial Data Analysis.
