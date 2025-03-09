from importers.base_importer import BaseImporter
from models import Application, RecruitmentCycle
from datetime import datetime

class ApplicationImporter(BaseImporter):
    
    def import_data(self, data_file):
        # Load data
        data = self._load_json(data_file)
        if not data:
            return False
        
        # Track statistics
        total_records = len(data)
        imported_count = 0
        skipped_count = 0
        error_count = 0

        # Process each application record
        for item in data:
            if not self._validate_application_data(item):
                skipped_count += 1
                continue
            
            # Find the cycle_id based on semester and year
            cycle_id = self._get_cycle_id(item.get('semester'), item.get('year'))
            if not cycle_id:
                self.logger.warning(f"Skipping application - no cycle found for {item.get('semester')} {item.get('year')}")
                skipped_count += 1
                continue
                
            # Check if application already exists
            existing = self._get_existing_application(item.get('title'), cycle_id)

            if existing:
                self.logger.info(f"Application '{item.get('title')}' already exists, updating...")
                result = self._update_application(existing, item, cycle_id)
            else:
                result = self._create_application(item, cycle_id)

            if result:
                imported_count += 1
            else:
                error_count += 1

        if imported_count > 0:
            try:
                self.session.commit()
                self.logger.info(f"Successfully committed {imported_count} application records")
            except Exception as e:
                self.logger.error(f"Error committing application data: {e}")
                self.session.rollback()
                return False

        self.logger.info(f"Application import summary: {imported_count} imported, {skipped_count} skipped, {error_count} errors out of {total_records} total")

        return imported_count > 0

    def _validate_application_data(self, item):
        """
        Validate application data
        
        Args:
            item: Dictionary containing application data
            
        Returns:
            bool: True if data is valid, False otherwise
        """
        required_fields = ['title', 'semester', 'year', 'published_time', 'closed_time', 'review_completion_time']
        
        for field in required_fields:
            if not item.get(field):
                self.logger.warning(f"Skipping application with missing {field}")
                return False
                
        return True
    
    def _get_cycle_id(self, semester, year):
        """
        Get the cycle_id for the given semester and year
        
        Args:
            semester: Semester string
            year: Year integer
            
        Returns:
            int: cycle_id if found, None otherwise
        """
        try:
            cycle = self.session.query(RecruitmentCycle).filter(
                RecruitmentCycle.semester == semester,
                RecruitmentCycle.year == year
            ).first()
            
            if cycle:
                return cycle.cycle_id
            else:
                self.logger.warning(f"No recruitment cycle found for {semester} {year}")
                return None
        except Exception as e:
            self.logger.error(f"Error finding cycle for {semester} {year}: {e}")
            return None
    
    def _get_existing_application(self, title, cycle_id):
        """
        Check if an application already exists
        
        Args:
            title: Application title
            cycle_id: Cycle ID
            
        Returns:
            Application: Existing application object if found, None otherwise
        """
        try:
            existing = self.session.query(Application).filter(
                Application.title == title,
                Application.cycle_id == cycle_id
            ).first()
            
            return existing
        except Exception as e:
            self.logger.error(f"Error checking for existing application: {e}")
            return None
    
    def _parse_datetime(self, datetime_str):
        """
        Parse datetime string to datetime object
        
        Args:
            datetime_str: Datetime string in format 'YYYY-MM-DD HH:MM:SS'
            
        Returns:
            datetime: Parsed datetime object
        """
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            self.logger.error(f"Error parsing datetime {datetime_str}: {e}")
            return None
    
    def _create_application(self, item, cycle_id):
        """
        Create a new application record
        
        Args:
            item: Dictionary containing application data
            cycle_id: Cycle ID to associate with this application
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Parse datetime strings
            published_time = self._parse_datetime(item.get('published_time'))
            closed_time = self._parse_datetime(item.get('closed_time'))
            review_completion_time = self._parse_datetime(item.get('review_completion_time'))
            
            if not all([published_time, closed_time, review_completion_time]):
                self.logger.error(f"Failed to parse datetime for application {item.get('title')}")
                return False
            
            application = Application(
                title=item.get('title'),
                active=item.get('active', False),
                created_time=published_time,  # Using published_time as created_time
                closed_time=closed_time,
                review_completion_time=review_completion_time,
                cycle_id=cycle_id
            )

            # Add to session
            self.session.add(application)
            self.logger.info(f"Created new application: '{item.get('title')}'")
            return True
        except Exception as e:
            self.logger.error(f"Error creating application: {e}")
            return False
        
    def _update_application(self, existing, item, cycle_id):
        """
        Update an existing application record
        
        Args:
            existing: Existing application object
            item: Dictionary containing updated application data
            cycle_id: Cycle ID to associate with this application
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Parse datetime strings
            published_time = self._parse_datetime(item.get('published_time'))
            closed_time = self._parse_datetime(item.get('closed_time'))
            review_completion_time = self._parse_datetime(item.get('review_completion_time'))
            
            if not all([published_time, closed_time, review_completion_time]):
                self.logger.error(f"Failed to parse datetime for application {item.get('title')}")
                return False
            
            existing.title = item.get('title')
            existing.active = item.get('active', False)
            existing.created_time = published_time  # Using published_time as created_time
            existing.closed_time = closed_time
            existing.review_completion_time = review_completion_time
            existing.cycle_id = cycle_id

            self.logger.info(f"Updated application: '{item.get('title')}'")
            return True
        except Exception as e:
            self.logger.error(f"Error updating application: {e}")
            return False