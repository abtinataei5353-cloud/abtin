# Abtin - Professional Crypto Trading Analysis Platform

A modular, production-ready Python desktop application for cryptocurrency trading analysis featuring TradingView-like interface with advanced technical analysis tools and RTM (Read The Market) concepts.

## Features

### Chart & Visualization
- **Interactive Candlestick Charts** - Smooth zooming, panning, and responsive design
- **Multiple Timeframes** - 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M
- **Dark Modern UI** - Professional theme with customizable appearance
- **Responsive Layout** - Adaptive panels and resizable components

### Technical Analysis Tools
- **Fibonacci** - Retracement and extensions
- **Trend Lines** - Auto-detection and manual drawing
- **Support/Resistance** - Horizontal and vertical lines
- **Price Channels** - Parallel line tools
- **Elliott Wave** - Wave pattern marking

### Advanced Technical Analysis
- **Fair Value Gaps (FVG)** - Gap identification and levels
- **Order Blocks** - Market structure zones
- **Break of Structure (BOS)** - Structure breaks and invalidations
- **Change of Character (CHoCH)** - Market behavior shifts
- **Liquidity Zones** - Liquidity cluster identification
- **Supply & Demand** - Zone detection and strength analysis
- **Market Structure** - HH/LH/LL/HL analysis
- **Volume Analysis** - Volume profile and clustering

### RTM (Read The Market) Concepts
- **Base, Decision, Rally, Drop** - Market phases
- **Flag Limit** - consolidation patterns
- **Quasimodo (QM)** - quick reversal patterns
- **Compression** - volatility squeeze zones
- **Engulf** - engulfing pattern detection
- **Momentum** - momentum analysis
- **Swap Levels** - level recovery detection
- **Flip Zones** - zone flips and confirmations

### Analysis Output
- **Entry Zones** - Precise entry point identification with context
- **Stop Loss Levels** - Risk management with multiple placement options
- **Take Profit Targets** - Multi-level TP targets with ratios
- **Confidence Score** - Evidence-based confidence rating (0-100%)
- **Factor Breakdown** - Clear explanation of contributing factors

### Multi-Exchange Support
- **Binance** - Spot and futures
- **Kraken** - Spot and derivatives
- **Coinbase Pro** - Spot trading
- **Gate.io** - Spot and futures
- **Bybit** - Perpetual futures
- Extensible architecture for additional exchanges

## Project Structure

```
abtin/
├── docs/                          # Comprehensive documentation
│   ├── ARCHITECTURE.md            # System design & module relationships
│   ├── API_EXCHANGE.md            # Exchange integration guide
│   ├── TECHNICAL_ANALYSIS.md      # Algorithm documentation
│   ├── RTM_METHODOLOGY.md         # RTM concepts explanation
│   └── DEVELOPMENT.md             # Setup & contribution guide
│
├── src/                           # Main application source code
│   ├── __init__.py
│   ├── main.py                    # Application entry point
│   │
│   ├── config/                    # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py            # Global settings & environment
│   │   ├── constants.py           # Application constants
│   │   └── logger_config.py       # Logging configuration
│   │
│   ├── data/                      # Data access & exchange integration
│   │   ├── __init__.py
│   │   ├── exchange_manager.py    # Multi-exchange abstraction layer
│   │   ├── candle_cache.py        # Caching & performance
│   │   ├── websocket_manager.py   # Real-time data streaming
│   │   │
│   │   └── exchanges/             # Exchange-specific implementations
│   │       ├── __init__.py
│   │       ├── base_exchange.py   # Abstract base class
│   │       ├── binance_exchange.py
│   │       ├── kraken_exchange.py
│   │       ├── coinbase_exchange.py
│   │       ├── gate_exchange.py
│   │       └── bybit_exchange.py
│   │
│   ├── analysis/                  # Technical analysis engine
│   │   ├── __init__.py
│   │   ├── analyzer.py            # Main analysis orchestrator
│   │   ├── result_builder.py      # Analysis result construction
│   │   │
│   │   ├── indicators/            # Technical indicators
│   │   │   ├── __init__.py
│   │   │   ├── price_levels.py    # Support/resistance detection
│   │   │   ├── fibonacci.py       # Fibonacci calculations
│   │   │   ├── volume.py          # Volume analysis
│   │   │   ├── volatility.py      # Volatility metrics
│   │   │   └── momentum.py        # Momentum indicators
│   │   │
│   │   ├── structures/            # Market structure analysis
│   │   │   ├── __init__.py
│   │   │   ├── fvg.py             # Fair Value Gaps
│   │   │   ├── order_blocks.py    # Order block detection
│   │   │   ├── liquidity.py       # Liquidity zones
│   │   │   ├── supply_demand.py   # Supply/demand zones
│   │   │   ├── market_structure.py # HH/LH/LL/HL analysis
│   │   │   └── bos_choch.py       # Break of structure, CHoCH
│   │   │
│   │   ├── patterns/              # Pattern recognition
│   │   │   ├── __init__.py
│   │   │   ├── trend_lines.py     # Trend line detection
│   │   │   ├── engulfing.py       # Engulfing patterns
│   │   │   ├── quasimodo.py       # Quasimodo patterns
│   │   │   └── elliott_wave.py    # Elliott wave counting
│   │   │
│   │   └── rtm/                   # Read The Market concepts
│   │       ├── __init__.py
│   │       ├── base_decision_rally_drop.py
│   │       ├── compression.py
│   │       ├── flag_limit.py
│   │       ├── momentum.py
│   │       ├── swap_levels.py
│   │       └── flip_zones.py
│   │
│   ├── ui/                        # User interface layer
│   │   ├── __init__.py
│   │   ├── main_window.py         # Main application window
│   │   ├── styles.py              # UI styling & themes
│   │   │
│   │   ├── widgets/               # Reusable UI components
│   │   │   ├── __init__.py
│   │   │   ├── chart_widget.py    # Chart display widget
│   │   │   ├── settings_panel.py  # Settings configuration
│   │   │   ├── analysis_panel.py  # Analysis results display
│   │   │   └── tools_panel.py     # Drawing tools interface
│   │   │
│   │   ├── charts/                # Chart rendering & interaction
│   │   │   ├── __init__.py
│   │   │   ├── chart_renderer.py  # Chart drawing & rendering
│   │   │   ├── zoom_pan.py        # Zoom/pan functionality
│   │   │   ├── candle_drawer.py   # Candlestick rendering
│   │   │   └── tools_drawer.py    # Drawing tools rendering
│   │   │
│   │   └── dialogs/               # Modal dialogs
│   │       ├── __init__.py
│   │       ├── exchange_config.py
│   │       └── indicator_settings.py
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       ├── math_utils.py          # Mathematical utilities
│       ├── cache.py               # Caching helpers
│       ├── async_utils.py         # Async/await utilities
│       └── validators.py          # Input validation
│
├── tests/                         # Comprehensive test suite
│   ├── __init__.py
│   ├── conftest.py                # pytest fixtures
│   ├── test_exchange_manager.py
│   ├── test_analyzer.py
│   ├── test_fibonacci.py
│   ├── test_fvg.py
│   ├── test_order_blocks.py
│   ├── test_bos_choch.py
│   ├── test_rtm_concepts.py
│   ├── test_chart_rendering.py
│   └── integration/               # Integration tests
│       ├── test_full_analysis_flow.py
│       └── test_exchange_integration.py
│
├── scripts/                       # Development & utility scripts
│   ├── setup_dev.sh               # Development environment setup
│   ├── seed_test_data.py          # Test data generation
│   ├── benchmark.py               # Performance benchmarking
│   └── generate_docs.py           # Documentation generation
│
├── requirements.txt               # Python dependencies
├── requirements-dev.txt           # Development dependencies
├── pyproject.toml                 # Project metadata & configuration
├── setup.py                       # Package installation
├── Makefile                       # Development commands
├── .env.example                   # Environment variables template
├── .gitignore
└── LICENSE
