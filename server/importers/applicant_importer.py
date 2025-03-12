from importers.base_importer import BaseImporter
from models import Applicant

class ApplicantImporter(BaseImporter):
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

        #process each applicant record
        for item in data:
            if not self._validate_applicant_data(item):
                skipped_count += 1
                continue

            existing = self._get_existing_record(
                Applicant,
                uin=item.get('UIN')
            )

            if existing:
                self.logger.info(f"Applicant '{item.get('UIN')} already exists, updating ...")
                result = self._update_applicant(existing, item)
            else:
                result = self._create_applicant(item)

            if result:
                imported_count += 1
            else:
                error_count += 1

        if imported_count > 0:
            try:
                self.session.commit()
                self.logger.info(f"Successfully committed {imported_count} applicant records")
            except Exception as e:
                self.logger.error(f"Error committing applicant data: {e}")
                return False

        self.logger.info(f"Applicant import summary: {imported_count} imported, {skipped_count} skipped, {error_count} errors out of {total_records} total")

        return imported_count > 0

    def _validate_applicant_data(self, item):
        """
        Validate applicant data
        
        Args:
            item: Dictionary containing applicant data
            
        Returns:
            bool: True if data is valid, False otherwise
        """

        if not item.get('UIN'):
            self.logger.warning("Skipping applicant with missing UIN")
            return False
        
        if not item.get('Email'):
            self.logger.warning(f"Skipping applicant '{item.get('UIN')}' with missing email")
            return False
        
        if not item.get('Major'):
            self.logger.warning(f"Skipping applicant '{item.get('UIN')}' with missing major")
            return False
        
        if not item.get('Grad Semester'):
            self.logger.warning(f"Skipping applicant '{item.get('UIN')}' with missing grad semester")
            return False
        
        if not item.get('Grad Year'):
            self.logger.warning(f"Skipping applicant '{item.get('UIN')}' with missing grad year")
            return False
        
        if not item.get('Admission'):
            self.logger.warning(f"Skipping applicant '{item.get('UIN')}' with missing admission status")
            return False

        return True
    
    def _create_applicant(self, item):
        """
        Create a new applicant record
        
        Args:
            item: Dictionary containing applicant data
            
        Returns:
            bool: True if successful, False otherwise
        """

        try:
            applicant = Applicant(
                uin=item.get('UIN'),
                email=item.get('Email'),
                major=item.get('Major'),
                grad_sem=item.get('Grad Semester'),
                grad_year=item.get('Grad Year'),
                admission=item.get('Admission')
            )

            #add to session
            self.session.add(applicant)
            self.logger.info(f"Created new applicant: '{item.get('UIN')}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating applicant '{item.get('UIN')}: {e}")
            return False
        
    def _update_applicant(self, existing, item):
        """
        Update an existing applicant record
        
        Args:
            existing: Existing applicant object
            item: Dictionary containing updated applicant data
            
        Returns:
            bool: True if successful, False otherwise
        """

        try:
            existing.uin=item.get('UIN')
            existing.email=item.get('Email')
            existing.major=item.get('Major')
            existing.grad_sem=item.get('Grad Semester')
            existing.grad_year=item.get('Grad Year')
            existing.admission=item.get('Admission')

            self.logger.info(f"Updated applicant: '{item.get('UIN')}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating applicant '{item.get('UIN')} : {e}")
            return False