"""
Technical Indicators Module
Calculates various technical indicators for market analysis.
"""

import pandas as pd
import numpy as np
import sqlite3
import logging
from typing import Tuple, Dict
import config

logger = logging.getLogger(__name__)


class TechnicalIndicators:
    """Calculate technical indicators for trading signals."""
    
    @staticmethod
    def simple_moving_average(data: pd.Series, period: int) -> pd.Series:
        """Calculate Simple Moving Average (SMA)."""
        return data.rolling(window=period).mean()
    
    @staticmethod
    def exponential_moving_average(data: pd.Series, period: int) -> pd.Series:
        """Calculate Exponential Moving Average (EMA)."""
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def relative_strength_index(data: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI).
        
        RSI = 100 - (100 / (1 + RS))
        where RS = Average Gain / Average Loss
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence).
        
        Returns:
            Tuple of (MACD line, Signal line, MACD Histogram)
        """
        ema_fast = data.ewm(span=fast, adjust=False).mean()
        ema_slow = data.ewm(span=slow, adjust=False).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def bollinger_bands(data: pd.Series, period: int = 20, std_dev: int = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate Bollinger Bands.
        
        Returns:
            Tuple of (Upper Band, Middle Band, Lower Band)
        """
        middle = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()
        
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        
        return upper, middle, lower
    
    @staticmethod
    def average_true_range(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Average True Range (ATR)."""
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        
        return atr
    
    @staticmethod
    def volume_weighted_average_price(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> pd.Series:
        """Calculate Volume Weighted Average Price (VWAP)."""
        typical_price = (high + low + close) / 3
        vwap = (typical_price * volume).rolling(window=20).sum() / volume.rolling(window=20).sum()
        
        return vwap
    
    @staticmethod
    def stochastic_oscillator(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> Tuple[pd.Series, pd.Series]:
        """
        Calculate Stochastic Oscillator.
        
        Returns:
            Tuple of (%K, %D)
        """
        lowest_low = low.rolling(window=period).min()
        highest_high = high.rolling(window=period).max()
        
        k_percent = 100 * (close - lowest_low) / (highest_high - lowest_low)
        d_percent = k_percent.rolling(window=3).mean()
        
        return k_percent, d_percent
    
    @staticmethod
    def on_balance_volume(close: pd.Series, volume: pd.Series) -> pd.Series:
        """Calculate On-Balance Volume (OBV)."""
        obv = (np.sign(close.diff()) * volume).fillna(0).cumsum()
        return obv
    
    @staticmethod
    def accumulation_distribution_line(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> pd.Series:
        """Calculate Accumulation/Distribution Line."""
        clv = ((close - low) - (high - close)) / (high - low)
        ad = (clv * volume).cumsum()
        
        return ad
    
    @staticmethod
    def rate_of_change(data: pd.Series, period: int = 12) -> pd.Series:
        """Calculate Rate of Change (ROC)."""
        roc = (data.pct_change(periods=period)) * 100
        return roc
    
    @staticmethod
    def support_resistance(high: pd.Series, low: pd.Series, window: int = 20) -> Tuple[pd.Series, pd.Series]:
        """
        Identify support and resistance levels.
        
        Returns:
            Tuple of (Support levels, Resistance levels)
        """
        support = low.rolling(window=window).min()
        resistance = high.rolling(window=window).max()
        
        return support, resistance


class IndicatorCalculator:
    """Main class to calculate and store all indicators."""
    
    def __init__(self, db_path: str = config.DATABASE_PATH):
        """Initialize indicator calculator."""
        self.db_path = db_path
        self.indicators = TechnicalIndicators()
    
    def calculate_all_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate all technical indicators for the data.
        
        Args:
            data: Market data with OHLCV columns
        
        Returns:
            Data with calculated indicators
        """
        data = data.copy()
        
        # Moving Averages
        data['sma_20'] = self.indicators.simple_moving_average(data['close'], config.SHORT_MA_PERIOD)
        data['sma_50'] = self.indicators.simple_moving_average(data['close'], config.MEDIUM_MA_PERIOD)
        data['sma_200'] = self.indicators.simple_moving_average(data['close'], config.LONG_MA_PERIOD)
        
        data['ema_12'] = self.indicators.exponential_moving_average(data['close'], 12)
        data['ema_26'] = self.indicators.exponential_moving_average(data['close'], 26)
        
        # RSI
        data['rsi_14'] = self.indicators.relative_strength_index(data['close'], config.RSI_PERIOD)
        
        # MACD
        data['macd'], data['macd_signal'], data['macd_histogram'] = self.indicators.macd(
            data['close'],
            config.MACD_FAST_PERIOD,
            config.MACD_SLOW_PERIOD,
            config.MACD_SIGNAL_PERIOD
        )
        
        # Bollinger Bands
        data['bb_upper'], data['bb_middle'], data['bb_lower'] = self.indicators.bollinger_bands(
            data['close'],
            config.BB_PERIOD,
            config.BB_STD_DEV
        )
        
        # ATR
        data['atr_14'] = self.indicators.average_true_range(
            data['high'],
            data['low'],
            data['close'],
            14
        )
        
        # VWAP
        data['vwap'] = self.indicators.volume_weighted_average_price(
            data['high'],
            data['low'],
            data['close'],
            data['volume']
        )
        
        # Stochastic Oscillator
        data['stoch_k'], data['stoch_d'] = self.indicators.stochastic_oscillator(
            data['high'],
            data['low'],
            data['close']
        )
        
        # OBV
        data['obv'] = self.indicators.on_balance_volume(data['close'], data['volume'])
        
        # A/D Line
        data['ad_line'] = self.indicators.accumulation_distribution_line(
            data['high'],
            data['low'],
            data['close'],
            data['volume']
        )
        
        # ROC
        data['roc_12'] = self.indicators.rate_of_change(data['close'], 12)
        
        # Support/Resistance
        data['support'], data['resistance'] = self.indicators.support_resistance(
            data['high'],
            data['low']
        )
        
        return data
    
    def calculate_ma_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate moving average crossover signals.
        
        Args:
            data: Data with SMA indicators
        
        Returns:
            Data with MA signal columns
        """
        data = data.copy()
        
        # Golden Cross / Death Cross (20/200 MA)
        data['ma_crossover_signal'] = 0
        data.loc[data['sma_20'] > data['sma_200'], 'ma_crossover_signal'] = 1
        data.loc[data['sma_20'] < data['sma_200'], 'ma_crossover_signal'] = -1
        
        # Crossover events
        data['ma_golden_cross'] = (
            (data['ma_crossover_signal'] == 1) & 
            (data['ma_crossover_signal'].shift(1) != 1)
        ).astype(int)
        
        data['ma_death_cross'] = (
            (data['ma_crossover_signal'] == -1) & 
            (data['ma_crossover_signal'].shift(1) != -1)
        ).astype(int)
        
        return data
    
    def calculate_rsi_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate RSI-based signals.
        
        Args:
            data: Data with RSI indicator
        
        Returns:
            Data with RSI signal columns
        """
        data = data.copy()
        
        data['rsi_oversold'] = (data['rsi_14'] < config.RSI_OVERSOLD).astype(int)
        data['rsi_overbought'] = (data['rsi_14'] > config.RSI_OVERBOUGHT).astype(int)
        
        # RSI bullish/bearish
        data['rsi_trend'] = 0
        data.loc[data['rsi_14'] > 50, 'rsi_trend'] = 1
        data.loc[data['rsi_14'] < 50, 'rsi_trend'] = -1
        
        return data
    
    def calculate_volume_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate volume-based signals.
        
        Args:
            data: Market data with volume
        
        Returns:
            Data with volume signal columns
        """
        data = data.copy()
        
        # Volume MA
        data['volume_ma'] = data['volume'].rolling(window=config.VOLUME_SMA_PERIOD).mean()
        
        # Volume above/below MA
        data['volume_signal'] = 0
        data.loc[data['volume'] > data['volume_ma'], 'volume_signal'] = 1
        data.loc[data['volume'] < data['volume_ma'], 'volume_signal'] = -1
        
        return data
    
    def save_indicators_to_db(self, data: pd.DataFrame, symbol: str):
        """Save calculated indicators to database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for _, row in data.iterrows():
                cursor.execute("""
                    INSERT OR REPLACE INTO indicators 
                    (symbol, date, sma_20, sma_50, sma_200, rsi_14, macd, macd_signal, macd_histogram, bb_upper, bb_middle, bb_lower, atr_14)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    symbol,
                    row['date'].strftime("%Y-%m-%d") if isinstance(row['date'], pd.Timestamp) else row['date'],
                    row.get('sma_20'),
                    row.get('sma_50'),
                    row.get('sma_200'),
                    row.get('rsi_14'),
                    row.get('macd'),
                    row.get('macd_signal'),
                    row.get('macd_histogram'),
                    row.get('bb_upper'),
                    row.get('bb_middle'),
                    row.get('bb_lower'),
                    row.get('atr_14')
                ))
            
            conn.commit()
            conn.close()
            logger.info(f"Saved {len(data)} indicator records for {symbol}")
        except Exception as e:
            logger.error(f"Error saving indicators: {e}")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    from data_processor import DataProcessor
    
    # Example usage
    processor = DataProcessor()
    data = processor.fetch_market_data("AAPL", "2023-01-01", "2024-01-01")
    data = processor.preprocess_data(data)
    
    calc = IndicatorCalculator()
    data = calc.calculate_all_indicators(data)
    data = calc.calculate_ma_signals(data)
    data = calc.calculate_rsi_signals(data)
    data = calc.calculate_volume_signals(data)
    
    print(data[['date', 'close', 'sma_20', 'sma_200', 'rsi_14', 'macd']].tail(10))
