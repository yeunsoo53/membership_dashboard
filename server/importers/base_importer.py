import json
import csv
import logging
from abc import ABC, abstractmethod

class BaseImporter(ABC):
    """
    Abstract base class for all data importers.
    Provides common methods for loading data from files and handling errors.
    """

    def __init__(self, session):
        """
        Initialize importer with a database session
        """
        self.session = session
        self.logger = logging.getLogger(f'db_population.{self.__class__.__name__}')

    @abstractmethod
    def import_data(self, data_file):
        """
        Import data from file to database
        
        Args:
            data_file: Path to the data file
            
        Returns:
            bool: True if import was successful, False otherwise
        """
        pass

    def _load_json(self, file_path):
        try: 
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading JSON file {file_path}: {e}")
            return None
    
    def _load_csv(self, file_path):
        try:
            data = []
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader :
                    data.append(row)
            return data
        except Exception as e:
            self.logger.error(f"Error loading CSV file {file_path}: {e}")
            return None

    def _safe_execute(self, operation_name, operation_func, *args, **kwargs):
        """
        Execute a database operation safely within a try-except block
        
        Args:
            operation_name: Name of the operation (for logging)
            operation_func: Function to execute
            *args, **kwargs: Arguments to pass to the function
            
        Returns:
            The result of operation_func, or None if an error occurred
        """
        try:
            result = operation_func(*args, **kwargs)
            return result
        except Exception as e:
            self.logger.error(f'Error during {operation_name}: {e}')
            self.session.rollback()
            return None
        
    def _get_existing_record(self, model_class, **filters):
        """
        Check if a record already exists in the database
        
        Args:
            model_class: SQLAlchemy model class
            **filters: Keyword arguments for filtering records
            
        Returns:
            model_class instance if found, None otherwise
        """

        try:
            return self.session.query(model_class).filter_by(**filters).first()
        except Exception as e:
            self.logger.error(f"Erorr checking for existing record: {e}")
            return None