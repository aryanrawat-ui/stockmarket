# Stock Market Prediction System

## Live Demo

### Frontend Application (Streamlit UI)

🔗 Streamlit App: https://stockmarket-fvffmeurydhccidyfhowsc.streamlit.app/

Users can directly enter stock symbols and view prediction results through an interactive dashboard.

---

### Backend API (Render Deployment)

🔗 FastAPI Backend: https://stockmarketprediction-r270.onrender.com

### Important API Endpoints

- Health Check: /health
- Prediction API: /predict?ticker=RELIANCE.NS

---

## Project Overview

This project is a Machine Learning-based Stock Market Prediction System developed to analyze stock price movement and generate useful prediction-based insights for investors and learners.

The system performs:

- Future Closing Price Prediction using Linear Regression
- Buy / Hold / Sell Signal Generation using Logistic Regression

The project uses real-time stock market data fetched through yFinance and applies feature engineering techniques to improve prediction accuracy and overall model performance.

To make the project more practical and user-friendly, the prediction system was also connected to a simple interactive frontend using Streamlit so users can easily enter stock symbols and view prediction results without manually running code.

---

## Why I Built This Project

During college, I had a minor subject related to the Stock Market, and that made me deeply interested in understanding how stock analysis and prediction actually work.

Instead of only studying theory, I wanted to build something practical where I could apply both stock market concepts and machine learning together.

That is when I decided to create a Stock Market Prediction System that could perform technical analysis and prediction using real market data.

This project helped me combine:

- Stock market knowledge
- Machine learning fundamentals
- Data analysis
- API integration
- Deployment
- User-facing application building

into one real-world project.

---

## Learning Process

Since I was still a beginner in Machine Learning, I first contacted my seniors for guidance. They advised me not to directly start with complex deep learning models and instead build strong fundamentals using:

- Linear Regression
- Logistic Regression

This helped me understand how prediction systems work from the base level before moving toward advanced models.

---

## Understanding the Models

### Linear Regression

Linear Regression is used for predicting continuous values.

In this project, it is used to predict the next closing price of a stock.

Example:

If today's closing price is ₹2500, the model predicts whether tomorrow’s price may become ₹2525 or ₹2470.

This helps in understanding the possible price movement of the stock.

---

### Logistic Regression

Logistic Regression is used for classification problems.

In this project, it helps generate practical trading signals such as:

- Buy
- Hold
- Sell

instead of only predicting price values.

This makes the project more useful for decision-making instead of just number prediction.

---

## Research and Learning Resources

To understand the complete Machine Learning workflow, I learned from multiple sources:

### Krish Naik’s YouTube Channel

I learned how real Machine Learning projects are structured, including:

- Data preprocessing
- Feature engineering
- Model training
- Accuracy checking
- R² Score
- MAE (Mean Absolute Error)
- Model evaluation techniques

This gave me a strong understanding of how practical ML projects are built.

---

### Zerodha Learning Resources

I also explored Zerodha’s stock market educational playlists and resources, which helped me understand the financial side of the project.

From there, I learned:

- Moving Average
- EMA (Exponential Moving Average)
- Lag Features
- Trend Analysis
- Technical Indicators
- Stock behavior analysis

This was important because stock prediction requires both finance understanding and ML understanding together.

---

### Additional YouTube Research

I also explored multiple YouTube resources specifically focused on:

- Feature engineering for stock market prediction
- Best indicators used in prediction models
- Improving model performance

This helped me improve the quality of my model significantly.

---

## Problem Statement

Initially, my college teacher advised me to focus mainly on analyzing the Closing Price of stocks because closing price is considered one of the strongest indicators in stock market prediction.

Although opening price and other values can also be included, closing price gives the strongest base for prediction.

So, I first started the project using only:

- Closing Price

as the main feature.

---

## Initial Model Performance

At first, the model performance was poor because I was using only one feature.

Results:

- Accuracy: around 30–40%
- R² Score: negative value

This clearly showed that real stock market prediction cannot be done using only one feature.

This became one of the biggest learning points of the entire project.

---

## Feature Engineering Improvements

After analyzing the poor results, I understood that proper Feature Engineering was necessary.

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

These features helped the model understand actual market behavior instead of relying only on raw closing price.

This significantly improved model performance.

---

## Final Model Performance

After applying proper feature engineering:

- Accuracy improved to around 70%
- R² Score improved to 0.8+

This was a major improvement and showed that strong feature engineering is often more important than simply using a more complex model.

Since stock markets are highly dynamic and affected by many unpredictable external factors such as:

- News
- Politics
- Global events
- Investor sentiment
- Economic announcements

achieving perfect prediction is unrealistic.

That is why achieving stable performance with a strong R² score was considered a successful outcome.

---

## Building the API and Frontend

After completing the model, I wanted to make the project usable like a real-world application instead of just a notebook-based ML project.

So I used:

- FastAPI for backend API development

This allowed me to create prediction endpoints like:

- `/predict`
- `/health`

where users could request stock predictions directly through an API.

Later, one of my seniors suggested using Streamlit because it allows developers to create interactive applications using very minimal code.

This was very useful because instead of writing complex frontend code, I could quickly build a simple and clean stock prediction dashboard where users can:

- Enter stock ticker symbols
- Get prediction results
- View buy / hold / sell outputs easily

I learned Streamlit through YouTube tutorials and practical implementation while building the project.

This made the project much more user-friendly and presentation-ready.

---

## Deployment

My friends suggested deploying the project on Render so that the project would become publicly accessible and could be shared with recruiters, teachers, and interviewers.

I deployed the FastAPI project on Render and made it live.

This added strong practical value to the project because it was no longer just local code—it became a real deployed application.

To improve reliability, I also added:

- `/health` endpoint
- Self-ping logic

to help maintain uptime and reduce sleeping issues on free hosting.

This made the project feel more production-ready.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- yFinance
- FastAPI
- Streamlit
- Render
- Machine Learning
- Feature Engineering
- Stock Market Technical Analysis

---

## API Endpoints

### Health Check

`/health`

Used to monitor whether the deployed API is active.

---

### Prediction Endpoint

`/predict?ticker=RELIANCE.NS`

Used to fetch stock prediction results for a given ticker symbol.

---

## Challenges Faced

### 1. Poor Initial Accuracy

Using only closing price resulted in poor accuracy and negative R² score.

This taught me the importance of strong feature engineering.

---

### 2. Understanding Technical Indicators

Learning financial indicators like EMA, Moving Averages, Lag Features, and Trend Strength required significant research because both stock market knowledge and ML understanding were needed together.

---

### 3. Deployment Problems

Deploying FastAPI on Render created dependency conflicts, API failures, and uptime problems.

This was solved using health checks and self-ping logic.

---

### 4. Stock Symbol Issues

Some stocks like BAJAJ.NS created ticker mismatch problems with yFinance.

Handling NSE stock symbols correctly was another practical challenge.

---

### 5. Converting ML Project into a Usable Product

Making the project accessible through APIs and Streamlit instead of keeping it limited to notebooks required additional learning and practical implementation.

This improved the overall quality of the project significantly.

---

## Key Learnings

This project taught me that:

- Real-world Machine Learning is mostly about data cleaning and feature engineering
- Simple models can perform very well when features are strong
- Deployment is often harder than model training
- Production-ready ML systems require monitoring and maintenance
- User accessibility matters as much as model accuracy
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
