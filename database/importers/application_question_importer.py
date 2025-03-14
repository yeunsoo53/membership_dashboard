from importers.base_importer import BaseImporter
from models import Question, RecruitmentCycle, Application, ApplicationQuestion, QuestionType

class AppQuestionImporter(BaseImporter):

    def import_data(self, question_file):
        #load data
        data = self._load_json(question_file)
        if not data:
            return False    

        stats = {
            "processed": 0,
            "created": 0,
            "errors": 0,
            "skipped": 0
        }

        try:
            #process each question in question file
            for question_data in data:
                stats["processed"] += 1 

                # question_type_str = question_data.get("type")
                question_type = QuestionType.APPLICATION
                # try:
                #     # Convert string to enum value
                #     question_type = QuestionType(question_type_str)
                # except ValueError:
                #     self.logger.error(f"Invalid question type: {question_type_str}")
                #     stats["errors"] += 1
                #     continue

                #get question text
                question = self._get_existing_record (
                    Question,
                    text=question_data.get("text"),
                    type=question_type
                )
                if not question:
                    self.logger.info(f"Question not found: {question}")
                    continue
                
                self.logger.info(f"question text: {question.text} question type: {question.type}")
                #get question id
                question_id = question.question_id

                #get cycles for the question
                cycles = question_data.get("cycle", [])
                self.logger.info(f"cycles: {cycles}")

                #get cycle data for each question
                for cycle_code in cycles:
                    semester = "Fall" if cycle_code[0].upper() == "F" else "Spring"
                    year = "20" + cycle_code[1:]

                    #get the matching cycle record
                    cycle = self._get_existing_record(
                        RecruitmentCycle,
                        semester=semester,
                        year=year
                    )

                    self.logger.info(f"Found cycle id for {cycle_code} : {cycle.cycle_id}")

                    if not cycle:
                        self.logger.error(f"Cycle not found: {semester} {year}")
                        stats["errors"] += 1
                        continue

                    #find application with matching cycle id
                    application = self._get_existing_record(
                        Application,
                        cycle_id=cycle.cycle_id
                    )

                    if not application:
                        self.logger.error(f"Application not found for cycle: {cycle_code}")
                        stats["errors"] += 1
                        continue

                    #check if record exists
                    existing = self._get_existing_record(
                        ApplicationQuestion,
                        app_id=application.app_id,
                        question_id=question_id
                    )

                    if existing:
                        self.logger.info(f"ApplicationQuestion already exists for application {application.app_id} and question {question_id}")
                        stats["skipped"] += 1
                        continue

                    #create new entry
                    try:
                        app_question = ApplicationQuestion (
                            app_id=application.app_id,
                            question_id=question_id
                        )

                        self.session.add(app_question)
                        self.session.commit()

                        stats["created"] += 1
                        self.logger.info(f"Created AplicationQuestion")

                    except Exception as e:
                        self.session.rollback()
                        self.logger.error(f"Error creating ApplicationQuestion: {e}")
                        stats["errors"] += 1
                        return False
        except Exception as e:
            self.logger.error(f"Error processing questions from json: {e}")
            stats["errors"] += 1

        self.logger.info(f"Processed {stats['processed']}; created {stats['created']}; skipped {stats['skipped']}; errors in {stats['errors']}")
        
        if stats["errors"] > 0:
            return False
        return True