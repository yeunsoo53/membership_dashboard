from importers.base_importer import BaseImporter
from models import Committee, CommitteeDivision

class CommitteeImporter(BaseImporter):
    
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

        #process each committee record
        for item in data:
            if not self._validate_committee_data(item):
                skipped_count += 1
                continue

            existing = self._get_existing_record(
                Committee,
                name=item.get('name')
            )

            if existing:
                self.logger.info(f"Committee '{item.get('name')} already exists, updating ...")
                result = self._update_committee(existing, item)
            else:
                result = self._create_committee(item)

            if result:
                imported_count += 1
            else:
                error_count += 1

        if imported_count > 0:
            try:
                self.session.commit()
                self.logger.info(f"Sucessfully committed {imported_count} committee records")
            except Exception as e:
                self.logger.error(f"Error committing committee data: {e}")
                return False

        self.logger.info(f"Committee import summary: {imported_count} imported, {skipped_count} skipped, {error_count} errors out of {total_records} total")

        return imported_count > 0

    def _validate_committee_data(self, item):
        """
        Validate committee data
        
        Args:
            item: Dictionary containing committee data
            
        Returns:
            bool: True if data is valid, False otherwise
        """

        if not item.get('name'):
            self.logger.warning("Skipping committee with missing name")
            return False
        
        if not item.get('division'):
            self.logger.warning(f"Skipping committee '{item.get('name')}' with missing division")
            return False
        
        #validate divison against enum
        try:
            CommitteeDivision[item.get('division')]
        except (KeyError, TypeError):
            self.logger.warning(f"Invalid division '{item.get('division')}' for committee '{item.get('name')}'. Skipping.")
            return False

        return True
    
    def _create_committee(self, item):
        """
        Create a new committee record
        
        Args:
            item: Dictionary containing committee data
            
        Returns:
            bool: True if successful, False otherwise
        """

        try:
            division = CommitteeDivision[item.get('division')]

            committee = Committee(
                name=item.get('name'),
                division=division
            )

            #add to session
            self.session.add(committee)
            self.logger.info(f"Created new committee: '{item.get('name')}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating committee '{item.get('name')}: {e}")
            return False
        
    def _update_committee(self, existing, item):
        """
        Update an existing committee record
        
        Args:
            existing: Existing Committee object
            item: Dictionary containing updated committee data
            
        Returns:
            bool: True if successful, False otherwise
        """

        try:
            division = item.get('division')

            existing.name = item.get('name')
            existing.division = division

            self.logger.info(f"Updated committee: '{item.get('name')}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating committee '{item.get('name')} : {e}")
            return False