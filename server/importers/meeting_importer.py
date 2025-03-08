from importers.base_importer import BaseImporter
from models import Meeting

class MeetingImporter(BaseImporter):
    
    def import_data(self, data_file):
        #load data
        data = self._load_csv(data_file)
        if not data:
            return False
        
        #track statistics
        total_records = len(data)
        imported_count = 0
        skipped_count = 0
        error_count = 0

        #process each meeting record
        for item in data:
            if not self._validate_meeting_data(item):
                skipped_count += 1
                continue

            existing = self._get_existing_record(
                Meeting,
                title=item.get('title')
            )

            if existing:
                self.logger.info(f"Meeting '{item.get('title')} already exists, updating ...")
                result = self._update_meeting(existing, item)
            else:
                result = self._create_meeting(item)

            if result:
                imported_count += 1
            else:
                error_count += 1

        if imported_count > 0:
            try:
                self.session.commit()
                self.logger.info(f"Successfully committed {imported_count} meeting records")
            except Exception as e:
                self.logger.error(f"Error committing meeting data: {e}")
                return False

        self.logger.info(f"Meeting import summary: {imported_count} imported, {skipped_count} skipped, {error_count} errors out of {total_records} total")

        return imported_count > 0

    def _validate_meeting_data(self, item):
        """
        Validate meeting data
        
        Args:
            item: Dictionary containing meeting data
            
        Returns:
            bool: True if data is valid, False otherwise
        """

        if not item.get('title'):
            self.logger.warning("Skipping meeting with missing title")
            return False
        
        if not item.get('description'):
            self.logger.warning(f"Skipping meeting '{item.get('title')}' with missing description")
            return False
        
        if not item.get('date'):
            self.logger.warning(f"Skipping meeting '{item.get('title')}' with missing date")
            return False
        
        if not item.get('location'):
            self.logger.warning(f"Skipping meeting '{item.get('title')}' with missing location")
            return False
        
        return True
    
    def _create_meeting(self, item):
        """
        Create a new meeting record
        
        Args:
            item: Dictionary containing meeting data
            
        Returns:
            bool: True if successful, False otherwise
        """

        try:
            meeting = Meeting(
                title=item.get('title'),
                description = item.get('description'),
                date = item.get('date'),
                location = item.get('location')
            )

            #add to session
            self.session.add(meeting)
            self.logger.info(f"Created new meeting: '{item.get('title')}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating meeting '{item.get('title')}: {e}")
            return False
        
    def _update_meeting(self, existing, item):
        """
        Update an existing meeting record
        
        Args:
            existing: Existing meeting object
            item: Dictionary containing updated meeting data
            
        Returns:
            bool: True if successful, False otherwise
        """

        try:
            existing.title = item.get('title')
            existing.description = item.get('description')
            existing.date = item.get('date')
            existing.location = item.get('location')

            self.logger.info(f"Updated meeting: '{item.get('title')}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating meeting '{item.get('title')} : {e}")
            return False