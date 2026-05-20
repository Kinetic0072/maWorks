"""
Data Processor Module
Handles loading, preprocessing, and feature engineering for market data.
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import sqlite3
import logging
from typing import Tuple, List, Dict, Optional
import config

logger = logging.getLogger(__name__)


class DataProcessor:
    """Handle data loading and preprocessing for trading system."""
    
    def __init__(self, db_path: str = config.DATABASE_PATH):
        """Initialize data processor."""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for market data storage."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create tables if they don't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    date TEXT NOT NULL,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    adj_close REAL,
                    UNIQUE(symbol, date)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS indicators (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    date TEXT NOT NULL,
                    sma_20 REAL,
                    sma_50 REAL,
                    sma_200 REAL,
                    rsi_14 REAL,
                    macd REAL,
                    macd_signal REAL,
                    macd_histogram REAL,
                    bb_upper REAL,
                    bb_middle REAL,
                    bb_lower REAL,
                    atr_14 REAL,
                    UNIQUE(symbol, date)
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def fetch_market_data(
        self, 
        symbol: str, 
        start_date: str = None, 
        end_date: str = None,
        use_cache: bool = True
    ) -> pd.DataFrame:
        """
        Fetch market data from yfinance or database cache.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            use_cache: Use cached data if available
        
        Returns:
            DataFrame with OHLCV data
        """
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=config.DEFAULT_LOOKBACK_DAYS)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        # Try to load from cache first
        if use_cache:
            cached_data = self._load_from_database(symbol, start_date, end_date)
            if cached_data is not None and len(cached_data) > 0:
                logger.info(f"Loaded {len(cached_data)} records for {symbol} from cache")
                return cached_data
        
        # Fetch from yfinance
        try:
            logger.info(f"Fetching {symbol} data from yfinance ({start_date} to {end_date})")
            data = yf.download(
                symbol, 
                start=start_date, 
                end=end_date,
                progress=False
            )
            
            if data is not None and len(data) > 0:
                data.reset_index(inplace=True)
                data.columns = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
                data['symbol'] = symbol
                
                # Store in database
                self._save_to_database(data)
                
                return data
            else:
                logger.warning(f"No data retrieved for {symbol}")
                return pd.DataFrame()
        
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    def _load_from_database(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Load data from SQLite database."""
        try:
            conn = sqlite3.connect(self.db_path)
            query = f"""
                SELECT date, open, high, low, close, adj_close, volume 
                FROM market_data 
                WHERE symbol = '{symbol}' 
                AND date BETWEEN '{start_date}' AND '{end_date}'
                ORDER BY date
            """
            data = pd.read_sql_query(query, conn)
            conn.close()
            
            if len(data) > 0:
                data['date'] = pd.to_datetime(data['date'])
                return data
            return None
        except Exception as e:
            logger.error(f"Database read error: {e}")
            return None
    
    def _save_to_database(self, data: pd.DataFrame):
        """Save market data to SQLite database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for _, row in data.iterrows():
                cursor.execute("""
                    INSERT OR IGNORE INTO market_data 
                    (symbol, date, open, high, low, close, volume, adj_close)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row['symbol'],
                    row['date'].strftime("%Y-%m-%d") if isinstance(row['date'], pd.Timestamp) else row['date'],
                    row['open'],
                    row['high'],
                    row['low'],
                    row['close'],
                    int(row['volume']),
                    row['adj_close']
                ))
            
            conn.commit()
            conn.close()
            logger.info(f"Saved {len(data)} records to database")
        except Exception as e:
            logger.error(f"Database write error: {e}")
    
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess data: handle missing values, outliers, normalization.
        
        Args:
            data: Raw market data
        
        Returns:
            Preprocessed data
        """
        if data is None or len(data) == 0:
            logger.warning("Empty data provided for preprocessing")
            return pd.DataFrame()
        
        data = data.copy()
        
        # Convert date to datetime
        if 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])
        
        # Handle missing values
        numeric_cols = ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        for col in numeric_cols:
            if col in data.columns:
                # Forward fill for OHLC data
                data[col].fillna(method='ffill', inplace=True)
                # Backward fill for any remaining NaNs
                data[col].fillna(method='bfill', inplace=True)
        
        # Remove duplicate rows
        data = data.drop_duplicates(subset=['date', 'symbol'] if 'symbol' in data.columns else ['date'])
        
        # Remove outliers using IQR method
        for col in numeric_cols:
            if col in data.columns and col != 'volume':
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                data[col] = data[col].clip(lower=lower_bound, upper=upper_bound)
        
        # Sort by date
        data = data.sort_values('date').reset_index(drop=True)
        
        logger.info(f"Data preprocessed: {len(data)} records")
        return data
    
    def create_train_test_split(
        self, 
        data: pd.DataFrame, 
        train_size: float = 0.8,
        test_size: float = 0.2
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split data into training and testing sets.
        
        Args:
            data: Preprocessed data
            train_size: Proportion for training
            test_size: Proportion for testing
        
        Returns:
            Tuple of (train_data, test_data)
        """
        split_idx = int(len(data) * train_size)
        return data.iloc[:split_idx], data.iloc[split_idx:]
    
    def create_sequences(
        self, 
        data: np.ndarray, 
        lookback: int = 60
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences for LSTM model training.
        
        Args:
            data: Input features
            lookback: Number of lookback periods
        
        Returns:
            Tuple of (X, y) sequences
        """
        X, y = [], []
        for i in range(len(data) - lookback):
            X.append(data[i:i + lookback])
            y.append(data[i + lookback])
        return np.array(X), np.array(y)
    
    def normalize_data(
        self, 
        data: pd.DataFrame,
        method: str = "minmax"
    ) -> Tuple[pd.DataFrame, Dict]:
        """
        Normalize numerical features.
        
        Args:
            data: Input data
            method: Normalization method (minmax, standard, robust)
        
        Returns:
            Normalized data and scaling parameters
        """
        data = data.copy()
        scaling_params = {}
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        if method == "minmax":
            for col in numeric_cols:
                min_val = data[col].min()
                max_val = data[col].max()
                data[col] = (data[col] - min_val) / (max_val - min_val + 1e-8)
                scaling_params[col] = {'min': min_val, 'max': max_val, 'type': 'minmax'}
        
        elif method == "standard":
            for col in numeric_cols:
                mean_val = data[col].mean()
                std_val = data[col].std()
                data[col] = (data[col] - mean_val) / (std_val + 1e-8)
                scaling_params[col] = {'mean': mean_val, 'std': std_val, 'type': 'standard'}
        
        elif method == "robust":
            for col in numeric_cols:
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                data[col] = (data[col] - Q1) / (IQR + 1e-8)
                scaling_params[col] = {'Q1': Q1, 'Q3': Q3, 'IQR': IQR, 'type': 'robust'}
        
        return data, scaling_params
    
    def inverse_normalize(
        self, 
        data: np.ndarray,
        scaling_params: Dict,
        column_name: str
    ) -> np.ndarray:
        """
        Reverse normalization to get original values.
        
        Args:
            data: Normalized data
            scaling_params: Scaling parameters from normalization
            column_name: Column name for which to reverse normalization
        
        Returns:
            Original scaled data
        """
        if column_name not in scaling_params:
            return data
        
        params = scaling_params[column_name]
        
        if params['type'] == 'minmax':
            return data * (params['max'] - params['min']) + params['min']
        elif params['type'] == 'standard':
            return data * params['std'] + params['mean']
        elif params['type'] == 'robust':
            return data * params['IQR'] + params['Q1']
        
        return data
    
    def add_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Add engineered features to the data.
        
        Args:
            data: Market data
        
        Returns:
            Data with additional features
        """
        data = data.copy()
        
        # Price-based features
        data['returns'] = data['close'].pct_change()
        data['log_returns'] = np.log(data['close'] / data['close'].shift(1))
        data['price_range'] = data['high'] - data['low']
        data['price_change'] = data['close'] - data['open']
        
        # Volume-based features
        data['volume_change'] = data['volume'].pct_change()
        data['volume_ma'] = data['volume'].rolling(config.VOLUME_SMA_PERIOD).mean()
        
        # Volatility features
        data['volatility'] = data['returns'].rolling(20).std()
        data['high_low_ratio'] = data['high'] / data['low']
        
        return data
    
    def get_multiple_symbols(
        self, 
        symbols: List[str],
        start_date: str = None,
        end_date: str = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple symbols.
        
        Args:
            symbols: List of stock symbols
            start_date: Start date
            end_date: End date
        
        Returns:
            Dictionary mapping symbols to DataFrames
        """
        data_dict = {}
        for symbol in symbols:
            try:
                data = self.fetch_market_data(symbol, start_date, end_date)
                if len(data) > 0:
                    data_dict[symbol] = self.preprocess_data(data)
                    logger.info(f"Successfully fetched data for {symbol}")
            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {e}")
        
        return data_dict


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    processor = DataProcessor()
    
    # Fetch data
    data = processor.fetch_market_data("AAPL", "2023-01-01", "2024-01-01")
    
    # Preprocess
    data = processor.preprocess_data(data)
    
    # Add features
    data = processor.add_features(data)
    
    print(data.head())
    print(f"\nData shape: {data.shape}")
    print(f"Columns: {list(data.columns)}")
