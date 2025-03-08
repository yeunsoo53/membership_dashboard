import os, sys, logging, argparse
from datetime import datetime
from sqlalchemy.orm import Session

from db_config import get_db
from importers import IMPORT_ORDER

def setup_logging(log_dir="logs"):
    """Set up logging configuration"""

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(
        log_dir,
        f"db_populaton_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger('db_population')

def parse_arguments():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description='Populate database from data files')

    parser.add_argument(
        '--data-dir', 
        dest='data_dir',
        default='data',
        help='Directory containing data files (default: data_files)'
    )

    parser.add_argument(
        '--log-dir',
        dest='log_dir',
        default='logs',
        help='Directory for log files (default: logs)'
    )

    parser.add_argument(
        '--importer',
        dest='specific_importer',
        help='Run only a specific importer (e.g., CommitteeImporter)'
    )

    return parser.parse_args()
    
def main():
    args = parse_arguments()

    logger = setup_logging(args.log_dir)
    logger.info(f"Starting database population from {args.data_dir}")

    #create database session
    try:
        db = next(get_db())
        logger.info("Successfully connected to database")
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        return 1
    
    #map of importer classes to datafiles
    data_files = {
        'CommitteeImporter': os.path.join(args.data_dir, "committee.json"),
        'PositionImporter': os.path.join(args.data_dir, "position.json")
    }

    #track success
    success_count = 0
    failure_count = 0

    #run importers in specific order
    importers_to_run = IMPORT_ORDER

    logger.info(f"Python path: {sys.path}")
    logger.info(f"Looking for importer: {args.specific_importer}")
    logger.info(f"Available importers: {[imp.__name__ for imp in IMPORT_ORDER]}")

    #if specific importer was requested, filter to just that one
    if args.specific_importer:
        importers_to_run = [imp for imp in IMPORT_ORDER if imp.__name__ == args.specific_importer]
        if not importers_to_run:
            logger.error(f"Importer '{args.specific_importer}' not found")
            return 1
        
    #run each importer
    for importer_class in importers_to_run:
        importer_name = importer_class.__name__
        data_file = data_files.get(importer_name)

        if not data_file:
            logger.warning(f"No data file specified for {importer_name}, skipping")
            continue

        logger.info(f"Starting import for {importer_name} from {data_file}")

        if not os.path.exists(data_file):
            logger.error(f"Data file not found: {data_file}")
            failure_count += 1
            return 1
        
        #create importer instance and run import
        importer = importer_class(db)
        success = importer.import_data(data_file)

        if success:
            logger.info(f"Successfully completed import for {importer_name}")
            success_count += 1
        else:
            logger.error(f"Failed to import data for {importer_name}")
            failure_count += 1

    logger.info(f"Import process completed: {success_count} successful, {failure_count} failed")

    db.close()

    return 0 if failure_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
            
    

