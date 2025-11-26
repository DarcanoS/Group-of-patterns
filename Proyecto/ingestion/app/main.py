"""
Main entry point for the ingestion service.

Usage:
    python -m app.main --mode historical
    python -m app.main --mode realtime (not implemented yet)
"""

import argparse
import sys
from pathlib import Path

from app.config import settings
from app.logging_config import setup_logging, get_logger
from app.db.session import get_db, test_connection
from app.services.ingestion_service import IngestionService

# Setup logging
logger = setup_logging(level=settings.ingestion_log_level)


def run_historical_ingestion():
    """
    Run one-time historical data ingestion from CSV files.
    
    This function:
    1. Tests database connectivity
    2. Creates ingestion service
    3. Processes all CSV files in data_air/
    4. Inserts readings into PostgreSQL
    """
    logger.info("=" * 70)
    logger.info("AIR QUALITY PLATFORM - HISTORICAL DATA INGESTION")
    logger.info("=" * 70)
    
    # Test database connection
    logger.info("\n[1/3] Testing database connection...")
    if not test_connection():
        logger.error("Database connection failed. Exiting.")
        sys.exit(1)
    
    # Create database session
    logger.info("\n[2/3] Initializing ingestion service...")
    db = next(get_db())
    
    try:
        service = IngestionService(db)
        service.preload_caches()
        
        # Run ingestion
        logger.info("\n[3/3] Running historical data ingestion...")
        stats = service.run_historical_ingestion()
        
        # Success
        logger.info("\n" + "✓" * 70)
        logger.info("Historical ingestion completed successfully!")
        logger.info("✓" * 70)
        
        return 0
        
    except Exception as e:
        logger.error(f"\n✗ Historical ingestion failed: {e}", exc_info=True)
        return 1
        
    finally:
        db.close()


def run_realtime_ingestion():
    """
    Run one-time real-time data ingestion from AQICN API.
    
    This function:
    1. Tests database connectivity
    2. Creates ingestion service with AQICN adapter
    3. Fetches current air quality data from AQICN
    4. Inserts readings into PostgreSQL
    """
    logger.info("=" * 70)
    logger.info("AIR QUALITY PLATFORM - REAL-TIME DATA INGESTION (AQICN)")
    logger.info("=" * 70)
    
    # Test database connection
    logger.info("\n[1/3] Testing database connection...")
    if not test_connection():
        logger.error("Database connection failed. Exiting.")
        sys.exit(1)
    
    # Create database session
    logger.info("\n[2/3] Initializing ingestion service...")
    db = next(get_db())
    
    try:
        service = IngestionService(db)
        service.preload_caches()
        
        # Run AQICN ingestion
        logger.info("\n[3/3] Running real-time data ingestion from AQICN API...")
        stats = service.run_aqicn_ingestion()
        
        # Success
        logger.info("\n" + "✓" * 70)
        logger.info("Real-time ingestion completed successfully!")
        logger.info("✓" * 70)
        
        return 0
        
    except Exception as e:
        logger.error(f"\n✗ Real-time ingestion failed: {e}", exc_info=True)
        return 1
        
    finally:
        db.close()


def main():
    """
    Main entry point with CLI argument parsing.
    """
    parser = argparse.ArgumentParser(
        description="Air Quality Platform - Data Ingestion Service",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run historical ingestion (one-time)
  python -m app.main --mode historical
  
  # Run real-time ingestion (periodic, not implemented yet)
  python -m app.main --mode realtime
        """
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['historical', 'realtime'],
        default='historical',
        help='Ingestion mode: historical (CSV files) or realtime (AQICN API)'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default=None,
        help='Override log level from config'
    )
    
    args = parser.parse_args()
    
    # Override log level if provided
    if args.log_level:
        global logger
        logger = setup_logging(level=args.log_level)
    
    # Route to appropriate handler
    if args.mode == 'historical':
        exit_code = run_historical_ingestion()
    elif args.mode == 'realtime':
        exit_code = run_realtime_ingestion()
    else:
        logger.error(f"Unknown mode: {args.mode}")
        exit_code = 1
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
