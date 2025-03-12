from importers.base_importer import BaseImporter
from models import Question, RecruitmentCycle, Application, ApplicationQuestion

class ApplicationQuestionImporter(BaseImporter):

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
            for question_data in data:
                stats["processed"] += 1

                question = self._get_existing_record (
                    Question,
                    text=question_data.get("text")
                )
                if not question:
                    self.logger.error(f"Question not found: {question}")
                    stats["errors"] += 1
                    continue

                question_id = question.id

                for cycle_code in question_data.get("cycles", []):
                    semester = "Fall" if cycle_code[0].upper() == "F" else "Spring"
                    year = "20" + cycle_code[1:]

                    cycle = self._get_existing_record(
                        RecruitmentCycle,
                        semester=semester,
                        year=year
                    )

                    if not cycle:
                        self.logger.error(f"Cycle not found: {semester} {year}")
                        stats["errors"] += 1
                        continue

                    #find application with matching cycle id
                    application = self._get_existing_record(
                        Application,
                        cycle_id=cycle.id
                    )

                    if not application:
                        self.logger.error(f"Application not found for cycle: {cycle_code}")
                        stats["errors"] += 1
                        continue

                    existing = self._get_existing_record(
                        ApplicationQuestion,
                        app_id=application.id,
                        question_id=question_id
                    )

                    if existing:
                        self.logger.info("ApplicationQuestion already exists for application {application.id} and question {quesiton_id}")
                        stats["skipped"] += 1
                        continue

                    #create new entry
                    try:
                        app_question = ApplicationQuestion (
                            app_id=application.id,
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
        except Exception as e:
            self.logger.error(f"Error processing questions from json: {e}")
            stats["errors"] += 1

        return stats