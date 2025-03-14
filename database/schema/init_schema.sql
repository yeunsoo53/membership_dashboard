-- Create tables from recruitment system
CREATE TABLE "recruitment_cycle"(
    "cycle_id" INTEGER NOT NULL,
    "semester" VARCHAR(255) NOT NULL,
    "year" INTEGER NOT NULL
);
ALTER TABLE "recruitment_cycle"
ADD PRIMARY KEY("cycle_id");
CREATE TABLE "applicant"(
    "applicant_id" INTEGER NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "major" VARCHAR(255) NOT NULL,
    "grad_sem" VARCHAR(255) NOT NULL,
    "grad_year" INTEGER NOT NULL,
    "recruitment_id" INTEGER NOT NULL,
    "admission" BOOLEAN NOT NULL
);
ALTER TABLE "applicant"
ADD PRIMARY KEY("applicant_id");
CREATE TABLE "application"(
    "app_id" INTEGER NOT NULL,
    "applicant_id" INTEGER NOT NULL,
    "active" BOOLEAN NOT NULL,
    "created_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "closed_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "review_completion_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "cycle_id" INTEGER NOT NULL
);
ALTER TABLE "application"
ADD PRIMARY KEY("app_id");
CREATE TABLE "app_question"(
    "app_question_id" INTEGER NOT NULL,
    "cycle_id" INTEGER NOT NULL,
    "question_text" TEXT NOT NULL,
    "max_score" INTEGER NOT NULL,
    "required" BOOLEAN NOT NULL
);
ALTER TABLE "app_question"
ADD PRIMARY KEY("app_question_id");
CREATE TABLE "app_response"(
    "app_response_id" INTEGER NOT NULL,
    "applicant_id" INTEGER NOT NULL,
    "question_id" INTEGER NOT NULL,
    "response_text" TEXT NOT NULL,
    "submission_date" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE "app_response"
ADD PRIMARY KEY("app_response_id");
-- Create tables from internal system
CREATE TABLE "mentorship_group"(
    "mentorship_id" INTEGER NOT NULL,
    "lead_mentor_id" INTEGER NOT NULL
);
ALTER TABLE "mentorship_group"
ADD PRIMARY KEY("mentorship_id");
-- Combined member table using the more complete version from internal
CREATE TABLE "member"(
    "member_id" INTEGER NOT NULL,
    "applicant_id" INTEGER NOT NULL,
    "phone" VARCHAR(255) NOT NULL,
    "cohort_sem" VARCHAR(255) NOT NULL,
    "cohort_year" INTEGER NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "standing" VARCHAR(255) NOT NULL,
    "mentorship_id" INTEGER NOT NULL
);
ALTER TABLE "member"
ADD PRIMARY KEY("member_id");
CREATE TABLE "position"(
    "position_id" INTEGER NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "level" VARCHAR(255) NOT NULL,
    "is_coordinator" BOOLEAN NOT NULL
);
ALTER TABLE "position"
ADD PRIMARY KEY("position_id");
CREATE TABLE "committee"(
    "committee_id" INTEGER NOT NULL,
    "name" VARCHAR(255) NULL,
    "division" VARCHAR(255) NULL
);
ALTER TABLE "committee"
ADD PRIMARY KEY("committee_id");
CREATE TABLE "member_history"(
    "history_id" INTEGER NOT NULL,
    "member_id" INTEGER NOT NULL,
    "position_id" INTEGER NOT NULL,
    "committee_id" INTEGER NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NULL
);
ALTER TABLE "member_history"
ADD PRIMARY KEY("history_id");
CREATE TABLE "committee_activity"(
    "activity_id" INTEGER NOT NULL,
    "committee_id" INTEGER NOT NULL,
    "date" DATE NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL
);
ALTER TABLE "committee_activity"
ADD PRIMARY KEY("activity_id");
CREATE TABLE "activity_attendance"(
    "attendance_id" INTEGER NOT NULL,
    "activity_id" INTEGER NOT NULL,
    "member_id" INTEGER NOT NULL,
    "present" BOOLEAN NOT NULL
);
ALTER TABLE "activity_attendance"
ADD PRIMARY KEY("attendance_id");
CREATE TABLE "event"(
    "event_id" INTEGER NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "category" VARCHAR(255) NOT NULL,
    "date" DATE NOT NULL,
    "location" VARCHAR(255) NOT NULL,
    "committee_id" INTEGER NULL,
    "description" TEXT NULL
);
ALTER TABLE "event"
ADD PRIMARY KEY("event_id");
CREATE TABLE "event_attendance"(
    "attendance_id" INTEGER NOT NULL,
    "event_id" INTEGER NOT NULL,
    "member_id" INTEGER NOT NULL,
    "present" BOOLEAN NOT NULL
);
ALTER TABLE "event_attendance"
ADD PRIMARY KEY("attendance_id");
CREATE TABLE "event_feedback"(
    "feedback_id" INTEGER NOT NULL,
    "event_id" INTEGER NOT NULL,
    "member_id" INTEGER NOT NULL,
    "rating" INTEGER NOT NULL,
    "comments" TEXT NULL
);
ALTER TABLE "event_feedback"
ADD PRIMARY KEY("feedback_id");
CREATE TABLE "mentorship_activity"(
    "activity_id" INTEGER NOT NULL,
    "mentorship_id" INTEGER NOT NULL,
    "date" DATE NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL
);
ALTER TABLE "mentorship_activity"
ADD PRIMARY KEY("activity_id");
CREATE TABLE "points"(
    "points_id" INTEGER NOT NULL,
    "member_id" INTEGER NOT NULL,
    "career_fair" INTEGER NOT NULL,
    "eng_dev" INTEGER NOT NULL,
    "social" INTEGER NOT NULL,
    "committee" INTEGER NOT NULL,
    "events" INTEGER NOT NULL,
    "outreach" INTEGER NOT NULL,
    "misc" INTEGER NOT NULL
);
ALTER TABLE "points"
ADD PRIMARY KEY("points_id");
CREATE TABLE "meeting"(
    "meeting_id" INTEGER NOT NULL,
    "title" INTEGER NOT NULL,
    "description" TEXT NOT NULL,
    "date" DATE NOT NULL
);
ALTER TABLE "meeting"
ADD PRIMARY KEY("meeting_id");
CREATE TABLE "meeting_attendance"(
    "attendance_id" INTEGER NOT NULL,
    "meeting_id" INTEGER NOT NULL,
    "member_id" INTEGER NOT NULL,
    "present" BOOLEAN NOT NULL
);
ALTER TABLE "meeting_attendance"
ADD PRIMARY KEY("attendance_id");
CREATE TABLE "slack_engagement"(
    "slack_id" INTEGER NOT NULL,
    "engagement" INTEGER NOT NULL,
    "member_id" INTEGER NOT NULL,
    "week_start_date" DATE NOT NULL,
    "week_end_date" DATE NOT NULL,
    "messages_sent" INTEGER NOT NULL,
    "reactions_given" INTEGER NOT NULL,
    "replies_sent" INTEGER NOT NULL,
    "threads_started" INTEGER NOT NULL,
    "active_channels" INTEGER NOT NULL
);
ALTER TABLE "slack_engagement"
ADD PRIMARY KEY("slack_id");
-- Continue with recruitment system tables
CREATE TABLE "reviewer"(
    "reviewer_id" INTEGER NOT NULL,
    "member_id" INTEGER NOT NULL,
    "cycle_id" INTEGER NOT NULL
);
ALTER TABLE "reviewer"
ADD PRIMARY KEY("reviewer_id");
CREATE TABLE "review_assignment"(
    "assignment_id" INTEGER NOT NULL,
    "applicant_id" INTEGER NOT NULL,
    "reviewer_id" INTEGER NOT NULL,
    "assigned_date" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "completed" BOOLEAN NOT NULL,
    "completed_date" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE "review_assignment"
ADD PRIMARY KEY("assignment_id");
CREATE TABLE "app_question_score"(
    "app_question_score_id" INTEGER NOT NULL,
    "assignment_id" INTEGER NOT NULL,
    "question_id" INTEGER NOT NULL,
    "response_id" INTEGER NOT NULL,
    "score" INTEGER NOT NULL,
    "comments" TEXT NOT NULL
);
ALTER TABLE "app_question_score"
ADD PRIMARY KEY("app_question_score_id");
CREATE TABLE "app_review"(
    "review_id" INTEGER NOT NULL,
    "app_id" INTEGER NOT NULL,
    "overall_score" INTEGER NOT NULL,
    "comments" TEXT NOT NULL,
    "recommendation" VARCHAR(255) NOT NULL
);
ALTER TABLE "app_review"
ADD PRIMARY KEY("review_id");
CREATE TABLE "interview"(
    "interview_id" INTEGER NOT NULL,
    "cycle_id" INTEGER NOT NULL,
    "app_id" INTEGER NOT NULL,
    "applicant_id" INTEGER NOT NULL,
    "overall_score" INTEGER NOT NULL,
    "decision" VARCHAR(255) NOT NULL,
    "comments" TEXT NOT NULL
);
ALTER TABLE "interview"
ADD PRIMARY KEY("interview_id");
CREATE TABLE "interview_question"(
    "interview_question_id" INTEGER NOT NULL,
    "cycle_id" INTEGER NOT NULL,
    "question_text" TEXT NOT NULL,
    "max_score" INTEGER NOT NULL
);
ALTER TABLE "interview_question"
ADD PRIMARY KEY("interview_question_id");
CREATE TABLE "interview_score"(
    "interview_score_id" INTEGER NOT NULL,
    "interview_id" INTEGER NOT NULL,
    "reviewer_id" INTEGER NOT NULL,
    "score" INTEGER NOT NULL
);
ALTER TABLE "interview_score"
ADD PRIMARY KEY("interview_score_id");
-- Add all foreign key constraints
-- From internal system
ALTER TABLE "points"
ADD CONSTRAINT "points_member_id_foreign" FOREIGN KEY("member_id") REFERENCES "member"("member_id");
ALTER TABLE "mentorship_activity"
ADD CONSTRAINT "mentorship_activity_mentorship_id_foreign" FOREIGN KEY("mentorship_id") REFERENCES "mentorship_group"("mentorship_id");
ALTER TABLE "event_feedback"
ADD CONSTRAINT "event_feedback_member_id_foreign" FOREIGN KEY("member_id") REFERENCES "member"("member_id");
ALTER TABLE "meeting_attendance"
ADD CONSTRAINT "meeting_attendance_meeting_id_foreign" FOREIGN KEY("meeting_id") REFERENCES "meeting"("meeting_id");
ALTER TABLE "slack_engagement"
ADD CONSTRAINT "slack_engagement_member_id_foreign" FOREIGN KEY("member_id") REFERENCES "member"("member_id");
ALTER TABLE "committee_activity"
ADD CONSTRAINT "committee_activity_committee_id_foreign" FOREIGN KEY("committee_id") REFERENCES "committee"("committee_id");
ALTER TABLE "member_history"
ADD CONSTRAINT "member_history_position_id_foreign" FOREIGN KEY("position_id") REFERENCES "position"("position_id");
ALTER TABLE "event"
ADD CONSTRAINT "event_committee_id_foreign" FOREIGN KEY("committee_id") REFERENCES "committee"("committee_id");
ALTER TABLE "member"
ADD CONSTRAINT "member_mentorship_id_foreign" FOREIGN KEY("mentorship_id") REFERENCES "mentorship_group"("mentorship_id");
ALTER TABLE "mentorship_group"
ADD CONSTRAINT "mentorship_group_lead_mentor_id_foreign" FOREIGN KEY("lead_mentor_id") REFERENCES "member"("member_id");
ALTER TABLE "member_history"
ADD CONSTRAINT "member_history_committee_id_foreign" FOREIGN KEY("committee_id") REFERENCES "committee"("committee_id");
ALTER TABLE "activity_attendance"
ADD CONSTRAINT "activity_attendance_activity_id_foreign" FOREIGN KEY("activity_id") REFERENCES "committee_activity"("activity_id");
ALTER TABLE "meeting_attendance"
ADD CONSTRAINT "meeting_attendance_member_id_foreign" FOREIGN KEY("member_id") REFERENCES "member"("member_id");
ALTER TABLE "event_attendance"
ADD CONSTRAINT "event_attendance_event_id_foreign" FOREIGN KEY("event_id") REFERENCES "event"("event_id");
ALTER TABLE "member_history"
ADD CONSTRAINT "member_history_member_id_foreign" FOREIGN KEY("member_id") REFERENCES "member"("member_id");
ALTER TABLE "event_attendance"
ADD CONSTRAINT "event_attendance_member_id_foreign" FOREIGN KEY("member_id") REFERENCES "member"("member_id");
ALTER TABLE "event_feedback"
ADD CONSTRAINT "event_feedback_event_id_foreign" FOREIGN KEY("event_id") REFERENCES "event"("event_id");
ALTER TABLE "activity_attendance"
ADD CONSTRAINT "activity_attendance_member_id_foreign" FOREIGN KEY("member_id") REFERENCES "member"("member_id");
-- From recruitment system
ALTER TABLE "review_assignment"
ADD CONSTRAINT "review_assignment_reviewer_id_foreign" FOREIGN KEY("reviewer_id") REFERENCES "reviewer"("reviewer_id");
ALTER TABLE "app_question_score"
ADD CONSTRAINT "app_question_score_question_id_foreign" FOREIGN KEY("question_id") REFERENCES "app_question"("app_question_id");
ALTER TABLE "interview"
ADD CONSTRAINT "interview_cycle_id_foreign" FOREIGN KEY("cycle_id") REFERENCES "recruitment_cycle"("cycle_id");
ALTER TABLE "app_response"
ADD CONSTRAINT "app_response_applicant_id_foreign" FOREIGN KEY("applicant_id") REFERENCES "applicant"("applicant_id");
ALTER TABLE "interview_score"
ADD CONSTRAINT "interview_score_reviewer_id_foreign" FOREIGN KEY("reviewer_id") REFERENCES "reviewer"("reviewer_id");
ALTER TABLE "application"
ADD CONSTRAINT "application_applicant_id_foreign" FOREIGN KEY("applicant_id") REFERENCES "applicant"("applicant_id");
ALTER TABLE "app_question"
ADD CONSTRAINT "app_question_cycle_id_foreign" FOREIGN KEY("cycle_id") REFERENCES "recruitment_cycle"("cycle_id");
ALTER TABLE "app_question_score"
ADD CONSTRAINT "app_question_score_response_id_foreign" FOREIGN KEY("response_id") REFERENCES "app_response"("app_response_id");
ALTER TABLE "review_assignment"
ADD CONSTRAINT "review_assignment_applicant_id_foreign" FOREIGN KEY("applicant_id") REFERENCES "applicant"("applicant_id");
ALTER TABLE "application"
ADD CONSTRAINT "application_cycle_id_foreign" FOREIGN KEY("cycle_id") REFERENCES "recruitment_cycle"("cycle_id");
ALTER TABLE "interview"
ADD CONSTRAINT "interview_app_id_foreign" FOREIGN KEY("app_id") REFERENCES "application"("app_id");
ALTER TABLE "app_response"
ADD CONSTRAINT "app_response_question_id_foreign" FOREIGN KEY("question_id") REFERENCES "app_question"("app_question_id");
ALTER TABLE "interview_question"
ADD CONSTRAINT "interview_question_cycle_id_foreign" FOREIGN KEY("cycle_id") REFERENCES "recruitment_cycle"("cycle_id");
ALTER TABLE "interview_score"
ADD CONSTRAINT "interview_score_interview_id_foreign" FOREIGN KEY("interview_id") REFERENCES "interview"("interview_id");
ALTER TABLE "app_question_score"
ADD CONSTRAINT "app_question_score_assignment_id_foreign" FOREIGN KEY("assignment_id") REFERENCES "review_assignment"("assignment_id");
ALTER TABLE "reviewer"
ADD CONSTRAINT "reviewer_member_id_foreign" FOREIGN KEY("member_id") REFERENCES "member"("member_id");
ALTER TABLE "member"
ADD CONSTRAINT "member_applicant_id_foreign" FOREIGN KEY("applicant_id") REFERENCES "applicant"("applicant_id");
ALTER TABLE "applicant"
ADD CONSTRAINT "applicant_recruitment_id_foreign" FOREIGN KEY("recruitment_id") REFERENCES "recruitment_cycle"("cycle_id");
ALTER TABLE "interview"
ADD CONSTRAINT "interview_applicant_id_foreign" FOREIGN KEY("applicant_id") REFERENCES "applicant"("applicant_id");
ALTER TABLE "app_review"
ADD CONSTRAINT "app_review_app_id_foreign" FOREIGN KEY("app_id") REFERENCES "application"("app_id");