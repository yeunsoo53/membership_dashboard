from importers.base_importer import BaseImporter
from models import RecruitmentCycle

class RecruitmentCycleImporter(BaseImporter):
    
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

        #process each cycle record
        for item in data:
            if not self._validate_cycle_data(item):
                skipped_count += 1
                continue

            existing = self._get_existing_record(
                RecruitmentCycle,
                semester=item.get('semester'),
                year=item.get('year')
            )

            if existing:
                self.logger.info(f"Cycle {item.get('semester')} {item.get('year')} already exists, updating ...")
                result = self._update_cycle(existing, item)
            else:
                result = self._create_cycle(item)

            if result:
                imported_count += 1
            else:
                error_count += 1

        if imported_count > 0:
            try:
                self.session.commit()
                self.logger.info(f"Successfully committed {imported_count} cycle records")
            except Exception as e:
                self.logger.error(f"Error committing cycle data: {e}")
                return False

        self.logger.info(f"Cycle import summary: {imported_count} imported, {skipped_count} skipped, {error_count} errors out of {total_records} total")

        return imported_count > 0

    def _validate_cycle_data(self, item):
        """
        Validate cycle data
        
        Args:
            item: Dictionary containing cycle data
            
        Returns:
            bool: True if data is valid, False otherwise
        """

        if not item.get('semester'):
            self.logger.warning("Skipping cycle with missing semester")
            return False
        
        if not item.get('year'):
            self.logger.warning(f"Skipping cycle with missing year")
            return False

        return True
    
    def _create_cycle(self, item):
        """
        Create a new cycle record
        
        Args:
            item: Dictionary containing cycle data
            
        Returns:
            bool: True if successful, False otherwise
        """

        try:
            cycle = RecruitmentCycle(
                semester=item.get('semester'),
                year=item.get('year')
            )

            #add to session
            self.session.add(cycle)
            self.logger.info(f"Created new cycle: {item.get('semester')} {item.get('year')}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating cycle {item.get('semester')} {item.get('year')}: {e}")
            return False
        
    def _update_cycle(self, existing, item):
        """
        Update an existing cycle record
        
        Args:
            existing: Existing cycle object
            item: Dictionary containing updated cycle data
            
        Returns:
            bool: True if successful, False otherwise
        """

        try:
            existing.semester = item.get('semester')
            existing.year = item.get('year')

            self.logger.info(f"Updated cycle: {item.get('semester')} {item.get('year')}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating cycle {item.get('semester')} {item.get('year')} : {e}")
            return False