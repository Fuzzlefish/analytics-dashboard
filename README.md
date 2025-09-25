
````markdown
# analytics-dashboard

This application fetches live stock data from Yahoo Finance and applies a time series predictive model to forecast stock performance. The results are displayed in an interactive web interface where you can:

Select different stocks from a dropdown menu.

Add additional stocks by updating the config file.

View all configured stocks together on a single comparison chart (scroll down in the app to see it).

## 🚀 Features
📈 Live stock data pulled directly from Yahoo Finance

🔮 Time series predictive modeling for stock price forecasting

🌐 Interactive web interface for exploring predictions

📊 Dropdown stock selection for quick access to individual tickers

⚙️ Configurable stock list – add more stocks by editing the config file

🖥️ Multi-stock comparison chart to visualize all configured stocks together

## 📦 Installation
Clone the repository and install dependencies in the dependency file:


```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
# Example: pip install -r requirements.txt, etc.
````

## 🛠 Usage

- Add whichever stock tickers you want to predict in the TICKERS array in the config.py file

```bash
# 
python -m src.update_data # make csv's of the live data
python -m src.webapp.app # hosts the webapp
```


## 🧪 Tests

Run tests with:

```bash
python -m pytest tests
```

## 🤝 Contributing

Contributions are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/awesome-feature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

