"""Tests for backtesting engine"""

import pytest
import pandas as pd
from src.backtesting.backtest_engine import BacktestEngine
from src.strategies.momentum_strategy import MomentumStrategy


class TestBacktestEngine:
    """Test backtesting engine."""
    
    @pytest.fixture
    def backtest_config(self):
        return {
            'initial_capital': 10000,
            'commission': 0.001,
            'slippage': 0.0005,
        }
    
    @pytest.fixture
    def engine(self, backtest_config):
        return BacktestEngine(backtest_config)
    
    @pytest.fixture
    def strategy(self):
        config = {
            'fast_period': 5,
            'slow_period': 10,
            'threshold': 0.02,
        }
        return MomentumStrategy(config)
    
    def test_engine_initialization(self, engine):
        assert engine.initial_capital == 10000
        assert engine.commission == 0.001
        assert engine.slippage == 0.0005
    
    def test_run_backtest(self, engine, strategy, sample_market_data):
        results = engine.run(strategy, sample_market_data, 'TEST')
        
        assert results is not None
        assert 'initial_capital' in results
        assert 'final_value' in results
        assert 'total_return' in results
        assert 'equity_curve' in results
    
    def test_results_structure(self, engine, strategy, sample_market_data):
        results = engine.run(strategy, sample_market_data, 'TEST')
        
        assert results['initial_capital'] == 10000
        assert isinstance(results['equity_curve'], list)
        assert len(results['equity_curve']) > 0
