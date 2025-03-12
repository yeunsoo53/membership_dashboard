from importers.base_importer import BaseImporter
from models import Position, PositionLevel

class PositionImporter(BaseImporter): 
    def import_data(self, data_file):
        #load data
        data = self._load_json(data_file)
        if not data:
            return False
        
        #track statistics
        total_records = len(data)
        imported_count = 0
        skipped_count = 0
        error_count = 0

        #process each position record
        for item in data:
            if not self._validate_position_data(item):
                skipped_count += 1
                continue

            existing = self._get_existing_record(
                Position,
                title=item.get('title')
            )

            if existing:
                self.logger.info(f"Position '{item.get('title')} already exists, updating ...")
                result = self._update_position(existing, item)
            else:
                result = self._create_position(item)

            if result:
                imported_count += 1
            else:
                error_count += 1

        if imported_count > 0:
            try:
                self.session.commit()
                self.logger.info(f"Successfully committed {imported_count} position records")
            except Exception as e:
                self.logger.error(f"Error committing position data: {e}")
                return False

        self.logger.info(f"Position import summary: {imported_count} imported, {skipped_count} skipped, {error_count} errors out of {total_records} total")

        return imported_count > 0

    def _validate_position_data(self, item):
        """
        Validate position data
        
        Args:
            item: Dictionary containing position data
            
        Returns:
            bool: True if data is valid, False otherwise
        """

        if not item.get('title'):
            self.logger.warning("Skipping position with missing title")
            return False
        
        if not item.get('level'):
            self.logger.warning(f"Skipping position '{item.get('title')}' with missing level")
            return False
        
        #validate divison against enum
        try:
            PositionLevel[item.get('level')]
        except (KeyError, TypeError):
            self.logger.warning(f"Invalid level '{item.get('level')}' for position '{item.get('title')}'. Skipping.")
            return False

        return True
    
    def _create_position(self, item):
        """
        Create a new position record
        
        Args:
            item: Dictionary containing position data
            
        Returns:
            bool: True if successful, False otherwise
        """

        try:
            level = PositionLevel[item.get('level')]

            position = Position(
                title=item.get('title'),
                level=level
            )

            #add to session
            self.session.add(position)
            self.logger.info(f"Created new position: '{item.get('title')}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating position '{item.get('title')}: {e}")
            return False
        
    def _update_position(self, existing, item):
        """
        Update an existing position record
        
        Args:
            existing: Existing position object
            item: Dictionary containing updated position data
            
        Returns:
            bool: True if successful, False otherwise
        """

        try:
            level = item.get('level')

            existing.title = item.get('title')
            existing.level = level

            self.logger.info(f"Updated position: '{item.get('title')}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating position '{item.get('title')} : {e}")
            return False