from importers.base_importer import BaseImporter
from models import Member, Applicant

class MemberImporter(BaseImporter):
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

        #process each member record
        for item in data:
            if not self._validate_member_data(item):
                skipped_count += 1
                continue

            existing = self._get_existing_record(
                Member,
                uin=item.get('uin')
            )

            if existing:
                self.logger.info(f"Member '{item.get('uin')} already exists, updating ...")
                result = self._update_member(existing, item)
            else:
                result = self._create_member(item)

            if result:
                imported_count += 1
            else:
                error_count += 1

        if imported_count > 0:
            try:
                self.session.commit()
                self.logger.info(f"Successfully committed {imported_count} member records")
            except Exception as e:
                self.logger.error(f"Error committing member data: {e}")
                return False

        self.logger.info(f"Member import summary: {imported_count} imported, {skipped_count} skipped, {error_count} errors out of {total_records} total")

        return imported_count > 0

    def _validate_member_data(self, item):
        """
        Validate member data
        
        Args:
            item: Dictionary containing member data
            
        Returns:
            bool: True if data is valid, False otherwise
        """

        if 'uin' not in item or item['uin'] is None or item['uin'] == '':
            self.logger.warning("Skipping member with missing uin")
            return False
        
        if 'Full Name' not in item or item['Full Name'] is None or item['Full Name'] == '':
            self.logger.warning(f"Skipping member '{item.get('uin')}' with missing name")
            return False
        
        if 'TAMU Email' not in item or item['TAMU Email'] is None or item['TAMU Email'] == '':
            self.logger.warning(f"Skipping member '{item.get('uin')}' with missing email")
            return False
        
        if 'Major' not in item or item['Major'] is None or item['Major'] == '':
            self.logger.warning(f"Skipping member '{item.get('uin')}' with missing major")
            return False
        
        if 'Expected Grad' not in item or item['Expected Grad'] is None or item['Expected Grad'] == '':
            self.logger.warning(f"Skipping member '{item.get('uin')}' with missing grad")
            return False
        
        if 'Instagram' not in item:
            self.logger.warning(f"Skipping member '{item.get('uin')}' with missing intagram")
            return False
        
        if 'LinkedIn' not in item:
            self.logger.warning(f"Skipping member '{item.get('uin')}' with missing linkedin")
            return False
        
        if 'Phone Number' not in item or item['Phone Number'] is None or item['Phone Number'] == '':
            self.logger.warning(f"Skipping member '{item.get('uin')}' with missing phone number")
            return False
        
        if 'Birthday Month' not in item or item['Birthday Month'] is None or item['Birthday Month'] == '':
            self.logger.warning(f"Skipping member '{item.get('uin')}' with missing birthday month")
            return False
        
        if 'Birthday Date' not in item or item['Birthday Date'] is None or item['Birthday Date'] == '':
            self.logger.warning(f"Skipping member '{item.get('uin')}' with missing birthday date")
            return False
        
        if 'Birthday Year' not in item or item['Birthday Year'] is None or item['Birthday Year'] == '':
            self.logger.warning(f"Skipping member '{item.get('uin')}' with missing birthday yea")
            return False

        return True
    
    def _create_member(self, item):
        """
        Create a new member record
        
        Args:
            item: Dictionary containing member data
            
        Returns:
            bool: True if successful, False otherwise
        """

        try:
            #find applicant id
            applicant = self._get_existing_record(
                Applicant,
                uin=item.get('uin')
            )

            if not applicant:
                self.logger.error(f"Application not found for member: {item.get('Full Name')} {item.get('uin')}")
            
            #parse name
            full_name = item.get('Full Name').split()
            first_name = full_name[0]
            last_name = full_name[1]

            #change phone number to a string
            phone_number = str(item.get('Phone Number'))[:10]

            #parse expected grad
            expected_grad = item.get('Expected Grad').split()
            grad_sem = expected_grad[0]
            grad_year = expected_grad[1]

            member = Member(  
                applicant_id=applicant.applicant_id,   
                first_name=first_name,
                last_name=last_name,           
                uin=item.get('uin'),
                tamu_email=item.get('TAMU Email'),
                phone=phone_number,
                major=item.get('Major'),
                cohort_sem=item.get('cohort_sem'),
                cohort_year=item.get('cohort_year'),
                grad_sem=grad_sem,
                grad_year=grad_year,
                is_active=True,
                probation=False,
                linkedin=item.get('LinkedIn'),
                insta=item.get('Instagram'),
                birthday_month = int(float(item.get('Birthday Month'))),
                birthday_day = int(float(item.get('Birthday Date'))),
                birthday_year = int(float(item.get('Birthday Year')))
            )

            #add to session
            self.session.add(member)
            self.logger.info(f"Created new member: {item.get('Full Name')}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating member {item.get('Full Name')}: {e}")
            return False
        
    def _update_member(self, existing, item):
        """
        Update an existing member record
        
        Args:
            existing: Existing member object
            item: Dictionary containing updated member data
            
        Returns:
            bool: True if successful, False otherwise
        """

        try:
             #parse name
            full_name = item.get('Full Name').split()
            first_name = full_name[0]
            last_name = full_name[1]

            #change phone number to a string
            phone_number = str(item.get('Phone Number'))[:10]

            #parse expected grad
            expected_grad = item.get('Expected Grad').split()
            grad_sem = expected_grad[0]
            grad_year = expected_grad[1]

            existing.first_name=first_name,
            existing.last_name=last_name,      
            existing.tamu_email=item.get('TAMU Email'),
            existing.phone=phone_number,
            existing.major=item.get('Major'),
            existing.cohort_sem=item.get('cohort_sem'),
            existing.cohort_year=item.get('cohort_year'),
            existing.grad_sem=grad_sem,
            existing.grad_year=grad_year,
            existing.linkedin=item.get('LinkedIn'),
            existing.insta=item.get('Instagram'),
            existing.birthday_month = int(float(item.get('Birthday Month'))),
            existing.birthday_day = int(float(item.get('Birthday Date'))),
            existing.birthday_year = int(float(item.get('Birthday Year')))

            self.logger.info(f"Updated applicant: {item.get('Full Name')} {item.get('uin')}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating applicant {item.get('Full Name')} {item.get('uin')} : {e}")
            return False