from sqlalchemy import Column, Integer, String, Boolean, Text, Date, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

class CommitteeName(enum.Enum):
    CAREER_FAIR = "Career Fair"
    CORPORATE = "Corporate Relations"
    ENG_DEV = "Engineering Development"
    FINANCE = "Finance"
    PROTRIP = "ProTrip"
    EWEEK = "EWeek"
    ENVISION = "Envision"
    PHILANTHROPY = "Philanthropy"
    SPECIAL_EVENTS = "Special Events"
    LEGISLATION = "Legislation"
    SAGR = "Society and Graduate Relations"
    STUDENT_RELATIONS = "Student Relations"
    IR = "Internal Relations"
    MARKETING = "Marketing"
    SYSAD = "Systems Administration"
    MEMBERSHIP = "Membership"

class CommitteeDivision(enum.Enum):
    DEVELOPMENT = "Development"
    EXTERNAL = "External"
    INTERNAL = "Internal"
    OPERATIONS = "Operations"

class PositionLevel(enum.Enum):
    GC = "General Council"
    EC = "Executive Council"
    EB = "Executive Board"

class QuestionType(enum.Enum):
    APPLICATION = "application"
    INTERVIEW = "interview"

class QuestionAudience(enum.Enum):
    MEMBER = "member"
    NON_MEMBER = "non_member"

Base = declarative_base()

# Recruitment system models
class RecruitmentCycle(Base):
    __tablename__ = "recruitment_cycle"
    
    cycle_id = Column(Integer, primary_key=True)
    semester = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    
    # Relationships
    applications = relationship("Application", back_populates="cycle")
    interviews = relationship("Interview", back_populates="cycle")
    reviewers = relationship("Reviewer", back_populates="cycle")

class Applicant(Base):
    __tablename__ = "applicant"
    
    applicant_id = Column(Integer, primary_key=True)
    uin = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    major = Column(String(255), nullable=False)
    grad_sem = Column(String(255), nullable=False)
    grad_year = Column(Integer, nullable=False)
    admission = Column(Boolean, nullable=False)
    
    # Relationships
    app_responses = relationship("AppResponse", back_populates="applicant")
    review_assignments = relationship("ReviewAssignment", back_populates="applicant")
    interviews = relationship("Interview", back_populates="applicant")
    member = relationship("Member", back_populates="applicant", uselist=False)

class Question(Base):
    __tablename__ = "question"

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    type = Column(Enum(QuestionType), nullable=False)
    audience = Column(Enum(QuestionAudience), nullable=False)
    word_limit = Column(Integer, nullable=True)
    max_score = Column(Integer, nullable=True)
    required = Column(Boolean, nullable=False)

    # Relationships
    application_questions = relationship("ApplicationQuestion", back_populates="question")
    interview_questions = relationship("InterviewQuestion", back_populates="question")

# class AppQuestion(Base):
#     __tablename__ = "app_question"
    
#     app_question_id = Column(Integer, primary_key=True)
#     cycle_id = Column(Integer, ForeignKey("recruitment_cycle.cycle_id"), nullable=False)
#     question_text = Column(Text, nullable=False)
#     max_score = Column(Integer, nullable=False)
#     required = Column(Boolean, nullable=False)
    
#     # Relationships
#     cycle = relationship("RecruitmentCycle", back_populates="app_questions")
#     responses = relationship("AppResponse", back_populates="question")
#     scores = relationship("AppQuestionScore", back_populates="question")

class AppResponse(Base):
    __tablename__ = "app_response"
    
    app_response_id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicant.applicant_id"), nullable=False)
    application_question_id = Column(Integer, ForeignKey("application_question.application_question_id"), nullable=False)
    response_text = Column(Text, nullable=False)
    submission_date = Column(DateTime, nullable=False)
    
    # Relationships
    applicant = relationship("Applicant", back_populates="app_responses")
    application_question = relationship("ApplicationQuestion", back_populates="responses")
    scores = relationship("AppQuestionScore", back_populates="response")

class Application(Base):
    __tablename__ = "application"
    
    app_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    active = Column(Boolean, nullable=False)
    created_time = Column(DateTime, nullable=False)
    closed_time = Column(DateTime, nullable=False)
    review_completion_time = Column(DateTime, nullable=False)
    cycle_id = Column(Integer, ForeignKey("recruitment_cycle.cycle_id"), nullable=False)
    
    # Relationships
    cycle = relationship("RecruitmentCycle", back_populates="applications")
    reviews = relationship("AppReview", back_populates="application")
    interviews = relationship("Interview", back_populates="application")
    questions = relationship("ApplicationQuestion", back_populates="application")

class ApplicationQuestion(Base):
    __tablename__ = "application_question"
    
    application_question_id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey("application.app_id"), nullable=False)
    question_id = Column(Integer, ForeignKey("question.question_id"), nullable=False)

    # Relationships
    application = relationship("Application", back_populates="questions")
    question = relationship("Question", back_populates="application_questions")
    responses = relationship("AppResponse", back_populates="application_question")
    scores = relationship("AppQuestionScore", back_populates="application_question")

class InterviewQuestion(Base):
    __tablename__ = "interview_question"
    
    interview_question_id = Column(Integer, primary_key=True)
    interview_id = Column(Integer, ForeignKey("interview.interview_id"), nullable=False)
    question_id = Column(Integer, ForeignKey("question.question_id"), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    
    # Relationships
    interview = relationship("Interview", back_populates="questions")
    question = relationship("Question", back_populates="interview_questions")
    scores = relationship("InterviewScore", back_populates="interview_question")

# Committee and Position models (no foreign key dependencies)
class Committee(Base):
    __tablename__ = "committee"
    
    committee_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    division = Column(Enum(CommitteeDivision), nullable=False)
    
    # Relationships
    member_history = relationship("MemberHistory", back_populates="committee")
    activities = relationship("CommitteeActivity", back_populates="committee")
    events = relationship("Event", back_populates="committee")

class Position(Base):
    __tablename__ = "position"
    
    position_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    level = Column(Enum(PositionLevel), nullable=False)
    
    # Relationships
    member_history = relationship("MemberHistory", back_populates="position")

class Meeting(Base):
    __tablename__ = "meeting"
    
    meeting_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String(255), nullable=False)
    
    # Relationships
    attendance = relationship("MeetingAttendance", back_populates="meeting")

class Event(Base):
    __tablename__ = "event"
    
    event_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String(255), nullable=False)
    committee_id = Column(Integer, ForeignKey("committee.committee_id"), nullable=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    committee = relationship("Committee", back_populates="events")
    attendance = relationship("EventAttendance", back_populates="event")
    feedback = relationship("EventFeedback", back_populates="event")

class CommitteeActivity(Base):
    __tablename__ = "committee_activity"
    
    activity_id = Column(Integer, primary_key=True)
    committee_id = Column(Integer, ForeignKey("committee.committee_id"), nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # Relationships
    committee = relationship("Committee", back_populates="activities")
    attendance = relationship("ActivityAttendance", back_populates="activity")

# Handle circular dependency between MentorshipGroup and Member
# First define both classes with minimal attributes

# class MentorshipGroup(Base):
#     __tablename__ = "mentorship_group"
    
#     mentorship_id = Column(Integer, primary_key=True)
#     lead_mentor_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)

class Member(Base):
    __tablename__ = "member"
    
    member_id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicant.applicant_id"), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    uin = Column(String(255), nullable=False)
    tamu_email = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    major = Column(String(255), nullable=False)
    cohort_sem = Column(String(255), nullable=False)
    cohort_year = Column(Integer, nullable=False)
    grad_sem = Column(String(255), nullable=False)
    grad_year = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)
    probation = Column(Boolean, nullable=False)
    # mentorship_id = Column(Integer, ForeignKey("mentorship_group.mentorship_id"), nullable=False)
    linkedin = Column(String(255), nullable=True)
    insta = Column(String(255), nullable=True)
    birthday_month = Column(Integer, nullable=False)
    birthday_day = Column(Integer, nullable=False)
    birthday_year = Column(Integer, nullable=False)

# Now add relationships
# MentorshipGroup.lead_mentor = relationship("Member", foreign_keys=[MentorshipGroup.lead_mentor_id], back_populates="led_mentorship")
# MentorshipGroup.members = relationship("Member", foreign_keys="Member.mentorship_id", back_populates="mentorship_group")
# MentorshipGroup.activities = relationship("MentorshipActivity", back_populates="mentorship")

Member.applicant = relationship("Applicant", back_populates="member")
# Member.mentorship_group = relationship("MentorshipGroup", foreign_keys=[Member.mentorship_id], back_populates="members")
# Member.led_mentorship = relationship("MentorshipGroup", foreign_keys="MentorshipGroup.lead_mentor_id", back_populates="lead_mentor", uselist=False)
Member.history = relationship("MemberHistory", back_populates="member")
Member.reviewer = relationship("Reviewer", back_populates="member")
Member.activity_attendance = relationship("ActivityAttendance", back_populates="member")
Member.event_attendance = relationship("EventAttendance", back_populates="member")
Member.event_feedback = relationship("EventFeedback", back_populates="member")
Member.meeting_attendance = relationship("MeetingAttendance", back_populates="member")
Member.points = relationship("Points", back_populates="member", uselist=False)
Member.slack_engagement = relationship("SlackEngagement", back_populates="member")

class MemberHistory(Base):
    __tablename__ = "member_history"
    
    history_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    position_id = Column(Integer, ForeignKey("position.position_id"), nullable=False)
    committee_id = Column(Integer, ForeignKey("committee.committee_id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    
    # Relationships
    member = relationship("Member", back_populates="history")
    position = relationship("Position", back_populates="member_history")
    committee = relationship("Committee", back_populates="member_history")

# class MentorshipActivity(Base):
#     __tablename__ = "mentorship_activity"
    
#     activity_id = Column(Integer, primary_key=True)
#     mentorship_id = Column(Integer, ForeignKey("mentorship_group.mentorship_id"), nullable=False)
#     date = Column(Date, nullable=False)
#     type = Column(String(255), nullable=False)
#     description = Column(Text, nullable=False)
    
#     # Relationships
#     mentorship = relationship("MentorshipGroup", back_populates="activities")

class ActivityAttendance(Base):
    __tablename__ = "activity_attendance"
    
    attendance_id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey("committee_activity.activity_id"), nullable=False)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    present = Column(Boolean, nullable=False)
    
    # Relationships
    activity = relationship("CommitteeActivity", back_populates="attendance")
    member = relationship("Member", back_populates="activity_attendance")

class EventAttendance(Base):
    __tablename__ = "event_attendance"
    
    attendance_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("event.event_id"), nullable=False)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    present = Column(Boolean, nullable=False)
    
    # Relationships
    event = relationship("Event", back_populates="attendance")
    member = relationship("Member", back_populates="event_attendance")

class EventFeedback(Base):
    __tablename__ = "event_feedback"
    
    feedback_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("event.event_id"), nullable=False)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comments = Column(Text, nullable=True)
    
    # Relationships
    event = relationship("Event", back_populates="feedback")
    member = relationship("Member", back_populates="event_feedback")

class MeetingAttendance(Base):
    __tablename__ = "meeting_attendance"
    
    attendance_id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meeting.meeting_id"), nullable=False)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    present = Column(Boolean, nullable=False)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="attendance")
    member = relationship("Member", back_populates="meeting_attendance")

class Points(Base):
    __tablename__ = "points"
    
    points_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    career_fair = Column(Integer, nullable=False)
    eng_dev = Column(Integer, nullable=False)
    social = Column(Integer, nullable=False)
    committee = Column(Integer, nullable=False)
    events = Column(Integer, nullable=False)
    outreach = Column(Integer, nullable=False)
    misc = Column(Integer, nullable=False)
    
    # Relationships
    member = relationship("Member", back_populates="points")

class SlackEngagement(Base):
    __tablename__ = "slack_engagement"
    
    slack_id = Column(Integer, primary_key=True)
    engagement = Column(Integer, nullable=False)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    week_start_date = Column(Date, nullable=False)
    week_end_date = Column(Date, nullable=False)
    messages_sent = Column(Integer, nullable=False)
    reactions_given = Column(Integer, nullable=False)
    replies_sent = Column(Integer, nullable=False)
    threads_started = Column(Integer, nullable=False)
    active_channels = Column(Integer, nullable=False)
    
    # Relationships
    member = relationship("Member", back_populates="slack_engagement")

# Recruitment system models (continued)
class Reviewer(Base):
    __tablename__ = "reviewer"
    
    reviewer_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False)
    cycle_id = Column(Integer, ForeignKey("recruitment_cycle.cycle_id"), nullable=False)
    
    # Relationships
    member = relationship("Member", back_populates="reviewer")
    cycle = relationship("RecruitmentCycle", back_populates="reviewers")
    assignments = relationship("ReviewAssignment", back_populates="reviewer")
    interview_scores = relationship("InterviewScore", back_populates="reviewer")

class ReviewAssignment(Base):
    __tablename__ = "review_assignment"
    
    assignment_id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicant.applicant_id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("reviewer.reviewer_id"), nullable=False)
    assigned_date = Column(DateTime, nullable=False)
    completed = Column(Boolean, nullable=False)
    completed_date = Column(DateTime, nullable=False)
    
    # Relationships
    applicant = relationship("Applicant", back_populates="review_assignments")
    reviewer = relationship("Reviewer", back_populates="assignments")
    question_scores = relationship("AppQuestionScore", back_populates="assignment")

class AppQuestionScore(Base):
    __tablename__ = "app_question_score"
    
    app_question_score_id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("review_assignment.assignment_id"), nullable=False)
    application_question_id = Column(Integer, ForeignKey("application_question.application_question_id"), nullable=False)
    response_id = Column(Integer, ForeignKey("app_response.app_response_id"), nullable=False)
    score = Column(Integer, nullable=False)
    comments = Column(Text, nullable=False)
    
    # Relationships
    assignment = relationship("ReviewAssignment", back_populates="question_scores")
    application_question = relationship("ApplicationQuestion", back_populates="scores")
    response = relationship("AppResponse", back_populates="scores")

class AppReview(Base):
    __tablename__ = "app_review"
    
    review_id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey("application.app_id"), nullable=False)
    overall_score = Column(Integer, nullable=False)
    comments = Column(Text, nullable=False)
    recommendation = Column(String(255), nullable=False)
    
    # Relationships
    application = relationship("Application", back_populates="reviews")

class Interview(Base):
    __tablename__ = "interview"
    
    interview_id = Column(Integer, primary_key=True)
    cycle_id = Column(Integer, ForeignKey("recruitment_cycle.cycle_id"), nullable=False)
    app_id = Column(Integer, ForeignKey("application.app_id"), nullable=False)
    applicant_id = Column(Integer, ForeignKey("applicant.applicant_id"), nullable=False)
    title = Column(String(255), nullable=False)
    overall_score = Column(Integer, nullable=False)
    decision = Column(String(255), nullable=False)
    comments = Column(Text, nullable=False)
    
    # Relationships
    cycle = relationship("RecruitmentCycle", back_populates="interviews")
    application = relationship("Application", back_populates="interviews")
    applicant = relationship("Applicant", back_populates="interviews")
    questions = relationship("InterviewQuestion", back_populates="interview")
    scores = relationship("InterviewScore", back_populates="interview")

class InterviewScore(Base):
    __tablename__ = "interview_score"
    
    interview_score_id = Column(Integer, primary_key=True)
    interview_id = Column(Integer, ForeignKey("interview.interview_id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("reviewer.reviewer_id"), nullable=False)
    interview_question_id = Column(Integer, ForeignKey("interview_question.interview_question_id"), nullable=False)
    score = Column(Integer, nullable=False)
    comments = Column(Text, nullable=True)
    
    # Relationships
    interview = relationship("Interview", back_populates="scores")
    reviewer = relationship("Reviewer", back_populates="interview_scores")
    interview_question = relationship("InterviewQuestion", back_populates="scores")

# Database connection code (optional)
# def init_db(db_url="postgresql://username:password@localhost:5432/membership_dashboard"):
#     engine = create_engine(db_url)
#     Session = sessionmaker(bind=engine)
    
#     # Create all tables in the database
#     Base.metadata.create_all(engine)
    
#     return engine, Session