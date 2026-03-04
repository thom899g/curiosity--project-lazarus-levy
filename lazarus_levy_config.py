"""
Configuration module for Project Lazarus Levy.
Centralizes all constants, thresholds, and exchange configurations.
Architectural Rationale: Centralized config prevents magic numbers,
enables easy adjustment of mission parameters, and supports
dynamic reloading in production scenarios.
"""

import os
from dataclasses import dataclass
from typing import Dict, List
from datetime import timedelta

@dataclass
class LazarusConfig:
    """Mission-critical configuration parameters"""
    
    # Financial targets
    TARGET_PROFIT: float = 27.40  # USD - Lightsail t3.nano daily cost
    MAX_POSITION_SIZE: float = 5.00  # USD per trade
    MIN_CONTRACT_PRICE: float = 0.000001  # Minimum price threshold
    MAX_CONTRACT_PRICE: float = 1.00  # Maximum price threshold
    
    # Trading parameters
    LEVERAGE: int = 5  # 5x leverage
    MAX_CONCURRENT_POSITIONS: int = 3
    STOP_LOSS_PERCENT: float = 2.0  # 2% stop loss
    TAKE_PROFIT_PERCENT: float = 5.0  # 5% take profit
    
    # Data collection
    SCRAPE_INTERVAL_SECONDS: int = 300  # 5 minutes
    SENTIMENT_WINDOW_MINUTES: int = 15
    VITALS_POLL_INTERVAL_SECONDS: int = 30
    
    # Firebase collections
    FIRESTORE_CONTRACTS_COLLECTION: str = "lazarus_contracts"
    FIRESTORE_TRADES_COLLECTION: str = "lazarus_trades"
    FIRESTORE_CORRELATIONS_COLLECTION: str = "lazarus_correlations"
    FIRESTORE_SYSTEM_STATE: str = "lazarus_system_state"
    
    # Exchange configurations
    SUPPORTED_EXCHANGES: List[str] = ["binance", "bybit", "okx", "kucoin"]
    
    # Risk management
    MAX_DAILY_LOSS_PERCENT: float = 10.0  # 10% max daily drawdown
    MIN_VOLUME_USD: float = 10000.0  # Minimum 24h volume
    MIN_LIQUIDITY_SCORE: float = 0.3  # Arbitrary liquidity score threshold
    
    # Model parameters
    CORRELATION_THRESHOLD: float = -0.7  # Strong negative correlation trigger
    MIN_DATA_POINTS: int = 50  # Minimum points for correlation calculation
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @property
    def get_scrape_interval(self) -> timedelta:
        """Return scrape interval as timedelta for scheduling"""
        return timedelta(seconds=self.SCRAPE_INTERVAL_SECONDS)

# Global configuration instance
config = LazarusConfig()

def validate_config() -> bool:
    """Validate configuration parameters for consistency"""
    try:
        assert config.TARGET_PROFIT > 0, "Target profit must be positive"
        assert config.MAX_POSITION_SIZE > 0, "Position size must be positive"
        assert config.MAX_POSITION_SIZE < 10, "Position size too large for mission"
        assert config.MIN_CONTRACT_PRICE < config.MAX_CONTRACT_PRICE, "Price range invalid"
        assert config.LEVERAGE >= 1 and config.LEVERAGE <= 10, "Leverage out of bounds"
        assert config.CORRELATION_THRESHOLD < 0, "Must seek negative correlation"
        return True