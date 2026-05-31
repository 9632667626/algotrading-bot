# AlgoTrading Bot

A comprehensive Python-based algorithmic trading bot designed for automated trading strategies, real-time market analysis, and portfolio management.

## Features

- **Multiple Trading Strategies**: Implement and backtest various trading strategies
- **Real-time Market Data**: Integration with market data providers
- **Risk Management**: Built-in position sizing and risk controls
- **Portfolio Management**: Track and manage multiple positions
- **Backtesting Engine**: Test strategies against historical data
- **Logging & Monitoring**: Comprehensive logging and performance metrics
- **Modular Architecture**: Easy to extend with new strategies and features
- **Telegram Integration**: Read trading signals from Telegram channels

## Project Structure

```
algotrading-bot/
├── src/
│   ├── strategies/              # Trading strategy implementations
│   │   ├── base_strategy.py
│   │   ├── momentum_strategy.py
│   │   └── mean_reversion_strategy.py
│   ├── market_data/            # Market data handlers
│   │   ├── data_provider.py
│   │   ├── live_data.py
│   │   └── historical_data.py
│   ├── execution/              # Order execution engine
│   ├── portfolio/              # Portfolio management
│   │   └── portfolio.py
│   ├── risk_management/        # Risk controls
│   │   └── risk_manager.py
│   ├── backtesting/            # Backtesting engine
│   │   └── backtest_engine.py
│   ├── integrations/           # External integrations
│   │   └── telegram_handler.py
│   ├── utils/                  # Utility functions
│   │   ├── logger.py
│   │   ├── config_loader.py
│   │   └── helpers.py
│   └── main.py                 # Main entry point
├── tests/                      # Test suite
├── config/                     # Configuration files
├── data/                       # Data storage
├── logs/                       # Log files
├── examples/                   # Example scripts
├── docs/                       # Documentation
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
├── pyproject.toml              # Project configuration
├── Makefile                    # Development commands
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip or conda
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/9632667626/algotrading-bot.git
cd algotrading-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Usage

### Running the Trading Bot

```bash
python src/main.py
```

### Running Backtests

```bash
python -m src.backtesting.backtest_engine --config config/config.yaml
```

### Running Tests

```bash
pytest tests/
```

### Development Commands

```bash
make help          # See all available commands
make format        # Format code
make lint          # Run linting
make test          # Run tests
make run           # Run the bot
```

## Configuration

Configuration files are in the `config/` directory:

- `config.yaml` - Main configuration
- `strategies.yaml` - Strategy parameters
- `telegram.yaml` - Telegram integration settings

## Telegram Integration

Read trading signals from Telegram channels:

```python
from src.integrations.telegram_handler import TelegramHandler
import asyncio

async def main():
    handler = TelegramHandler(config)
    await handler.connect()
    messages = await handler.get_channel_messages(limit=10)
    await handler.disconnect()

asyncio.run(main())
```

See [TELEGRAM_SETUP.md](docs/TELEGRAM_SETUP.md) for detailed setup instructions.

## Trading Strategies

### Momentum Strategy

Uses moving average crossovers to detect momentum shifts.

### Mean Reversion Strategy

Identifies overbought/oversold conditions using Bollinger Bands.

### Custom Strategies

Create your own by inheriting from `BaseStrategy`:

```python
from src.strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def calculate_signal(self, market_data):
        # Your logic here
        return 'BUY'  # or 'SELL' or 'HOLD'
```

## Testing

Run all tests:
```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## Risk Management

The bot includes:
- Position sizing based on account risk
- Stop loss calculation
- Take profit levels
- Daily loss limits
- Maximum position size limits

## Logging

Logs are stored in the `logs/` directory:
- File logs: `logs/trading_YYYYMMDD.log`
- Console output for real-time monitoring

## Contributing

1. Create a new branch for features/fixes
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Risk Disclaimer

⚠️ **This is an algorithmic trading bot for educational purposes.** Trading carries risk including potential loss of principal. Use with caution and always:
- Start with paper trading
- Test thoroughly on historical data
- Use appropriate position sizing and risk management
- Monitor trades actively
- Never invest money you can't afford to lose

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- Open an issue on GitHub
- Check the documentation in `docs/`
- Review example scripts in `examples/`

## Roadmap

- [ ] Live trading integration
- [ ] Multi-exchange support
- [ ] Advanced risk management
- [ ] Machine learning optimization
- [ ] Web dashboard
- [ ] Mobile app integration

---

**Happy Trading! 📈**