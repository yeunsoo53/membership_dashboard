from importers.base_importer import BaseImporter
from models import Question, QuestionType, QuestionAudience

class QuestionImporter(BaseImporter):
    
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

        # Process each question record
        for item in data:
            if not self._validate_question_data(item):
                skipped_count += 1
                continue

            existing = self._get_existing_record(
                Question,
                text=item.get('text'),
                type=QuestionType[item.get('type').upper()]
            )

            if existing:
                self.logger.info(f"Question '{item.get('text')[:30]}...' already exists, updating ...")
                result = self._update_question(existing, item)
            else:
                result = self._create_question(item)

            if result:
                imported_count += 1
            else:
                error_count += 1

        if imported_count > 0:
            try:
                self.session.commit()
                self.logger.info(f"Successfully committed {imported_count} question records")
            except Exception as e:
                self.logger.error(f"Error committing question data: {e}")
                return False

        self.logger.info(f"Question import summary: {imported_count} imported, {skipped_count} skipped, {error_count} errors out of {total_records} total")

        return imported_count > 0

    def _validate_question_data(self, item):
        """
        Validate question data
        
        Args:
            item: Dictionary containing question data
            
        Returns:
            bool: True if data is valid, False otherwise
        """
        if not item.get('text'):
            self.logger.warning("Skipping question with missing text")
            return False
        
        if not item.get('type'):
            self.logger.warning(f"Skipping question '{item.get('text')[:30]}...' with missing type")
            return False
        
        if not item.get('audience'):
            self.logger.warning(f"Skipping question '{item.get('text')[:30]}...' with missing audience")
            return False
        
        # Validate type against enum
        try:
            QuestionType[item.get('type').upper()]
        except (KeyError, TypeError):
            self.logger.warning(f"Invalid type '{item.get('type')}' for question '{item.get('text')[:30]}...'. Skipping.")
            return False

        # Validate audience against enum
        try:
            QuestionAudience[item.get('audience').upper()]
        except (KeyError, TypeError):
            self.logger.warning(f"Invalid audience '{item.get('audience')}' for question '{item.get('text')[:30]}...'. Skipping.")
            return False

        return True
    
    def _create_question(self, item):
        """
        Create a new question record
        
        Args:
            item: Dictionary containing question data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            question_type = QuestionType[item.get('type').upper()]
            audience = QuestionAudience[item.get('audience').upper()]

            question = Question(
                text=item.get('text'),
                type=question_type,
                audience=audience,
                word_limit=item.get('word_limit'),
                max_score=item.get('max_score'),
                required=item.get('required', True)
            )

            # Add to session
            self.session.add(question)
            self.logger.info(f"Created new question: '{item.get('text')[:30]}...'")
            return True
        except Exception as e:
            self.logger.error(f"Error creating question '{item.get('text')[:30]}...': {e}")
            return False
        
    def _update_question(self, existing, item):
        """
        Update an existing question record
        
        Args:
            existing: Existing question object
            item: Dictionary containing updated question data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            question_type = QuestionType[item.get('type').upper()]
            audience = QuestionAudience[item.get('audience').upper()]

            existing.text = item.get('text')
            existing.type = question_type
            existing.audience = audience
            existing.word_limit = item.get('word_limit')
            existing.max_score = item.get('max_score')
            existing.required = item.get('required', True)

            self.logger.info(f"Updated question: '{item.get('text')[:30]}...'")
            return True
        except Exception as e:
            self.logger.error(f"Error updating question '{item.get('text')[:30]}...': {e}")
            return False