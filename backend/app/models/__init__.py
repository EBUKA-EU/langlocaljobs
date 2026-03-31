
# Profile model: one-to-one with User
from datetime import datetime
from app.extension import db


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Single source of truth for permissions. Allowed values: user, recruiter, admin
    role = db.Column(db.String(50), default='user',
                     server_default='user', nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('profile', uselist=False))

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_recruiter(self):
        return self.role in ('recruiter', 'admin')


# models/__init__.py
#
# Defines SQLAlchemy models for User, Recruiter, Job, and SavedJob.


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    saved_jobs = db.relationship(
        'SavedJob', back_populates='user', cascade='all, delete-orphan')
    applied_jobs = db.relationship(
        'AppliedJob', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'


class Recruiter(db.Model):
    __tablename__ = 'recruiters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(255))
    user = db.relationship('User', backref=db.backref('recruiter', uselist=False))

    def __repr__(self):
        return f'<Recruiter {self.company_name}>'


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(120))
    location = db.Column(db.String(120))
    description = db.Column(db.Text)
    url = db.Column(db.String(255))
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    saved_by = db.relationship('SavedJob', back_populates='job',
                               cascade='all, delete-orphan')
    applied_by = db.relationship('AppliedJob', back_populates='job',
                                 cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Job {self.title}>'


class SavedJob(db.Model):
    __tablename__ = 'saved_jobs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='saved_jobs')
    job = db.relationship('Job', back_populates='saved_by')

    def __repr__(self):
        return f'<SavedJob user={self.user_id} job={self.job_id}>'


class AppliedJob(db.Model):
    __tablename__ = 'applied_jobs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='applied_jobs')
    job = db.relationship('Job', back_populates='applied_by')

    def __repr__(self):
        return f'<AppliedJob user={self.user_id} job={self.job_id}>'
