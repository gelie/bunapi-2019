# coding: utf-8
from sqlalchemy import Boolean, CheckConstraint, Column, Date, DateTime, ForeignKey, Index, Integer, LargeBinary, \
    Numeric, String, Table, Text, Time, UniqueConstraint
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Addres(db.Model):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'public'}

    address_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    principal_id = db.Column(db.ForeignKey('public.principal.principal_id'), nullable=False)
    logical_address_type = db.Column(db.String(128), nullable=False)
    postal_address_type = db.Column(db.String(128), nullable=False)
    street = db.Column(db.String(256))
    city = db.Column(db.String(256))
    zipcode = db.Column(db.String(20))
    country_id = db.Column(db.ForeignKey('public.country.country_id'))
    phone = db.Column(db.String(256))
    fax = db.Column(db.String(256))
    email = db.Column(db.String(512))
    status = db.Column(db.String(16))
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    country = db.relationship('Country', primaryjoin='Addres.country_id == Country.country_id', backref='address')
    principal = db.relationship('Principal', primaryjoin='Addres.principal_id == Principal.principal_id',
                                backref='address')


class AgendaAnalysisReport(db.Model):
    __tablename__ = 'agenda_analysis_report'
    __table_args__ = {'schema': 'public'}

    report_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    doc_id = db.Column(db.ForeignKey('public.doc.doc_id'), primary_key=True, nullable=False)
    title = db.Column(db.Text)
    outcomes = db.Column(db.Text)
    analysis = db.Column(db.Text)
    consideration_dates = db.Column(db.Text)
    atc_date = db.Column(db.DateTime, nullable=False)
    adoption_date = db.Column(db.DateTime, nullable=False)
    adoption_status = db.Column(db.Text)

    doc = db.relationship('Doc', primaryjoin='AgendaAnalysisReport.doc_id == Doc.doc_id',
                          backref='agenda_analysis_reports')


class AgendaTextRecord(db.Model):
    __tablename__ = 'agenda_text_record'
    __table_args__ = {'schema': 'public'}

    text_record_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text = db.Column(db.Text, nullable=False)
    record_type = db.Column(db.String(30), nullable=False)
    language = db.Column(db.String(5), nullable=False)


class Alfie(db.Model):
    __tablename__ = 'alfie'
    __table_args__ = {'schema': 'public'}

    alfie_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    head_id = db.Column(db.ForeignKey('public.doc.doc_id'), index=True)
    alfie_name = db.Column(db.Text, nullable=False)
    alfie_key = db.Column(db.Text, nullable=False)
    alfie_date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(7), nullable=False)
    sitting_id = db.Column(db.ForeignKey('public.sitting.sitting_id', match='FULL'))

    head = db.relationship('Doc', primaryjoin='Alfie.head_id == Doc.doc_id', backref='alfies')
    sitting = db.relationship('Sitting', primaryjoin='Alfie.sitting_id == Sitting.sitting_id', backref='alfies')


class Attachment(db.Model):
    __tablename__ = 'attachment'
    __table_args__ = {'schema': 'public'}

    attachment_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    head_id = db.Column(db.ForeignKey('public.doc.doc_id'), nullable=False, index=True)
    type = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    data = db.Column(db.String(32))
    name = db.Column(db.String(200))
    mimetype = db.Column(db.String(127))
    status = db.Column(db.String(48))
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    language = db.Column(db.String(5), nullable=False)

    head = db.relationship('Doc', primaryjoin='Attachment.head_id == Doc.doc_id', backref='attachments')


class Audit(db.Model):
    __tablename__ = 'audit'
    __table_args__ = {'schema': 'public'}

    audit_id = db.Column(db.Integer, primary_key=True)
    audit_type = db.Column(db.String(30), nullable=False)


class DebateRecordItemAudit(Audit):
    __tablename__ = 'debate_record_item_audit'
    __table_args__ = {'schema': 'public'}

    audit_id = db.Column(db.ForeignKey('public.audit.audit_id'), primary_key=True)
    debate_record_item_id = db.Column(db.ForeignKey('public.debate_record_item.debate_record_item_id'), nullable=False,
                                      index=True)
    debate_record_id = db.Column(db.Integer)
    type = db.Column(db.String(30), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    debate_record_item = db.relationship('DebateRecordItem',
                                         primaryjoin='DebateRecordItemAudit.debate_record_item_id == DebateRecordItem.debate_record_item_id',
                                         backref='debate_record_item_audits')


class DocAudit(Audit):
    __tablename__ = 'doc_audit'
    __table_args__ = {'schema': 'public'}

    audit_id = db.Column(db.ForeignKey('public.audit.audit_id'), primary_key=True)
    doc_id = db.Column(db.ForeignKey('public.doc.doc_id'), nullable=False, index=True)
    parliament_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(128), nullable=False)
    doc_type = db.Column(db.String(128))
    doc_procedure = db.Column(db.String(128))
    type_number = db.Column(db.Integer)
    registry_number = db.Column(db.String(128))
    uri = db.Column(db.String(1024))
    acronym = db.Column(db.String(48))
    title = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.Text)
    language = db.Column(db.String(5), nullable=False)
    body = db.Column(db.Text)
    original_text = db.Column(db.Text)
    status = db.Column(db.String(48))
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    group_id = db.Column(db.Integer)
    subject = db.Column(db.Text)
    coverage = db.Column(db.Text)
    geolocation = db.Column(db.Text)
    head_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    assignee_id = db.Column(db.Integer)

    doc = db.relationship('Doc', primaryjoin='DocAudit.doc_id == Doc.doc_id', backref='doc_audits')


t_change_tree = db.Table(
    'change_tree',
    db.Column('parent_id', db.ForeignKey('public.change.audit_id'), primary_key=True, nullable=False),
    db.Column('child_id', db.ForeignKey('public.change.audit_id'), primary_key=True, nullable=False),
    db.CheckConstraint('parent_id <> child_id'),
    schema='public'
)


class Change(Audit):
    __tablename__ = 'change'
    __table_args__ = {'schema': 'public'}

    audit_id = db.Column(db.ForeignKey('public.audit.audit_id'), primary_key=True)
    user_id = db.Column(db.ForeignKey('public.user.user_id'), nullable=False)
    action = db.Column(db.String(16), nullable=False)
    seq = db.Column(db.Integer, nullable=False)
    procedure = db.Column(db.String(1), nullable=False)
    date_audit = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    date_active = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    user = db.relationship('User', primaryjoin='Change.user_id == User.user_id', backref='changes')
    parents = db.relationship(
        'Change',
        secondary='public.change_tree',
        primaryjoin='Change.audit_id == change_tree.c.child_id',
        secondaryjoin='Change.audit_id == change_tree.c.parent_id',
        backref='changes'
    )


class SignatoryAudit(Audit):
    __tablename__ = 'signatory_audit'
    __table_args__ = {'schema': 'public'}

    audit_id = db.Column(db.ForeignKey('public.audit.audit_id'), primary_key=True)
    signatory_id = db.Column(db.ForeignKey('public.signatory.signatory_id'), nullable=False, index=True)
    head_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(32))

    signatory = db.relationship('Signatory', primaryjoin='SignatoryAudit.signatory_id == Signatory.signatory_id',
                                backref='signatory_audits')


class MinutesEmailAudit(Audit):
    __tablename__ = 'minutes_email_audit'
    __table_args__ = {'schema': 'public'}

    audit_id = db.Column(db.ForeignKey('public.audit.audit_id'), primary_key=True)
    minutes_email_id = db.Column(db.ForeignKey('public.minutes_email.minutes_email_id'), nullable=False, index=True)
    sitting_id = db.Column(db.Integer, nullable=False)
    sender = db.Column(db.Text)
    recipients = db.Column(db.Text)
    subject = db.Column(db.Text)
    message = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    minutes_email = db.relationship('MinutesEmail',
                                    primaryjoin='MinutesEmailAudit.minutes_email_id == MinutesEmail.minutes_email_id',
                                    backref='minutes_email_audits')


class AttachmentAudit(Audit):
    __tablename__ = 'attachment_audit'
    __table_args__ = {'schema': 'public'}

    audit_id = db.Column(db.ForeignKey('public.audit.audit_id'), primary_key=True)
    attachment_id = db.Column(db.ForeignKey('public.attachment.attachment_id'), nullable=False, index=True)
    head_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    data = db.Column(db.String(32))
    name = db.Column(db.String(200))
    mimetype = db.Column(db.String(127))
    status = db.Column(db.String(48))
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    language = db.Column(db.String(5), nullable=False)

    attachment = db.relationship('Attachment', primaryjoin='AttachmentAudit.attachment_id == Attachment.attachment_id',
                                 backref='attachment_audits')


class DebateRecordAudit(Audit):
    __tablename__ = 'debate_record_audit'
    __table_args__ = {'schema': 'public'}

    audit_id = db.Column(db.ForeignKey('public.audit.audit_id'), primary_key=True)
    debate_record_id = db.Column(db.ForeignKey('public.debate_record.debate_record_id'), nullable=False, index=True)
    sitting_id = db.Column(db.Integer, unique=True)
    status = db.Column(db.String(32))
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    debate_record = db.relationship('DebateRecord',
                                    primaryjoin='DebateRecordAudit.debate_record_id == DebateRecord.debate_record_id',
                                    backref='debate_record_audits')


t_bm_data_updates = db.Table(
    'bm_data_updates',
    db.Column('table_name', db.String(100), nullable=False),
    db.Column('action_type', db.String(10), nullable=False),
    db.Column('action_time', db.DateTime, nullable=False),
    db.Column('new_data', db.Text),
    db.Column('old_data', db.Text),
    schema='public'
)


class Country(db.Model):
    __tablename__ = 'country'
    __table_args__ = {'schema': 'public'}

    country_id = db.Column(db.String(2), primary_key=True)
    iso_name = db.Column(db.String(80), nullable=False)
    country_name = db.Column(db.String(80), nullable=False)
    iso3 = db.Column(db.String(3))
    numcode = db.Column(db.Integer)
    language = db.Column(db.String(5), nullable=False)


class CurrentlyEditingDocument(db.Model):
    __tablename__ = 'currently_editing_document'
    __table_args__ = {'schema': 'public'}

    user_id = db.Column(db.ForeignKey('public.user.user_id'), primary_key=True, nullable=False)
    currently_editing_id = db.Column(db.ForeignKey('public.doc.doc_id'), primary_key=True, nullable=False)
    editing_date = db.Column(db.DateTime)

    currently_editing = db.relationship('Doc',
                                        primaryjoin='CurrentlyEditingDocument.currently_editing_id == Doc.doc_id',
                                        backref='currently_editing_documents')
    user = db.relationship('User', primaryjoin='CurrentlyEditingDocument.user_id == User.user_id',
                           backref='currently_editing_documents')


t_debate_doc = db.Table(
    'debate_doc',
    db.Column('debate_doc_id', db.ForeignKey('public.debate_record_item.debate_record_item_id'), primary_key=True),
    db.Column('doc_id', db.ForeignKey('public.doc.doc_id')),
    schema='public'
)


class DebateMedia(db.Model):
    __tablename__ = 'debate_media'
    __table_args__ = {'schema': 'public'}

    debate_record_id = db.Column(db.ForeignKey('public.debate_record.debate_record_id'), primary_key=True,
                                 nullable=False)
    media_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    media_path = db.Column(db.Text, nullable=False)
    media_type = db.Column(db.String(100), nullable=False)

    debate_record = db.relationship('DebateRecord',
                                    primaryjoin='DebateMedia.debate_record_id == DebateRecord.debate_record_id',
                                    backref='debate_medias')


class DebateRecord(db.Model):
    __tablename__ = 'debate_record'
    __table_args__ = {'schema': 'public'}

    debate_record_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    sitting_id = db.Column(db.ForeignKey('public.sitting.sitting_id'), unique=True)
    status = db.Column(db.String(32))
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    sitting = db.relationship('Sitting', uselist=False, primaryjoin='DebateRecord.sitting_id == Sitting.sitting_id',
                              backref='debate_records')


class DebateRecordItem(db.Model):
    __tablename__ = 'debate_record_item'
    __table_args__ = {'schema': 'public'}

    debate_record_item_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    debate_record_id = db.Column(db.ForeignKey('public.debate_record.debate_record_id'))
    type = db.Column(db.String(30), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    debate_record = db.relationship('DebateRecord',
                                    primaryjoin='DebateRecordItem.debate_record_id == DebateRecord.debate_record_id',
                                    backref='debate_record_items')
    docs = db.relationship('Doc', secondary='public.debate_doc', backref='debate_record_items')


class DebateSpeech(DebateRecordItem):
    __tablename__ = 'debate_speech'
    __table_args__ = {'schema': 'public'}

    debate_speech_id = db.Column(db.ForeignKey('public.debate_record_item.debate_record_item_id'), primary_key=True)
    person_id = db.Column(db.ForeignKey('public.user.user_id'))
    text = db.Column(db.Text)
    status = db.Column(db.String(32))
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    language = db.Column(db.String(5), nullable=False)

    person = db.relationship('User', primaryjoin='DebateSpeech.person_id == User.user_id', backref='debate_speeches')


class DebateTake(db.Model):
    __tablename__ = 'debate_take'
    __table_args__ = {'schema': 'public'}

    debate_record_id = db.Column(db.ForeignKey('public.debate_record.debate_record_id'), primary_key=True,
                                 nullable=False)
    debate_take_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    transcriber_id = db.Column(db.ForeignKey('public.user.user_id'))
    debate_take_name = db.Column(db.String(100), nullable=False)

    debate_record = db.relationship('DebateRecord',
                                    primaryjoin='DebateTake.debate_record_id == DebateRecord.debate_record_id',
                                    backref='debate_takes')
    transcriber = db.relationship('User', primaryjoin='DebateTake.transcriber_id == User.user_id',
                                  backref='debate_takes')


class Doc(db.Model):
    __tablename__ = 'doc'
    __table_args__ = {'schema': 'public'}

    doc_id = db.Column(db.Integer, primary_key=True)
    parliament_id = db.Column(db.ForeignKey('public.parliament.parliament_id'))
    owner_id = db.Column(db.ForeignKey('public.user.user_id'), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    doc_type = db.Column(db.String(128))
    doc_procedure = db.Column(db.String(128))
    type_number = db.Column(db.Integer)
    registry_number = db.Column(db.String(128))
    uri = db.Column(db.String(1024))
    acronym = db.Column(db.String(48))
    title = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.Text)
    language = db.Column(db.String(5), nullable=False)
    body = db.Column(db.Text)
    original_text = db.Column(db.Text)
    status = db.Column(db.String(48), index=True)
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    group_id = db.Column(db.ForeignKey('public.group.group_id'))
    subject = db.Column(db.Text)
    coverage = db.Column(db.Text)
    geolocation = db.Column(db.Text)
    head_id = db.Column(db.ForeignKey('public.doc.doc_id'))
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    assignee_id = db.Column(db.Integer)

    group = db.relationship('Group', primaryjoin='Doc.group_id == Group.group_id', backref='group_docs')
    head = db.relationship('Doc', remote_side=[doc_id], primaryjoin='Doc.head_id == Doc.doc_id', backref='docs')
    owner = db.relationship('User', primaryjoin='Doc.owner_id == User.user_id', backref='user_docs')
    parliament = db.relationship('Parliament', primaryjoin='Doc.parliament_id == Parliament.parliament_id',
                                 backref='parliament_parliament_docs')
    users = db.relationship('User', secondary='public.user_doc', backref='user_docs_0')
    groups = db.relationship('Group', secondary='public.group_document_assignment', backref='group_docs_0')
    sittings = db.relationship('Sitting', secondary='public.sitting_report', backref='docs')


class EditorialNote(db.Model):
    __tablename__ = 'editorial_note'
    __table_args__ = {'schema': 'public'}

    editorial_note_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text = db.Column(db.Text)
    group_id = db.Column(db.ForeignKey('public.group.group_id'))
    language = db.Column(db.String(5), nullable=False)

    group = db.relationship('Group', primaryjoin='EditorialNote.group_id == Group.group_id', backref='editorial_notes')


class Eminute(db.Model):
    __tablename__ = 'eminutes'
    __table_args__ = {'schema': 'public'}

    eminutes_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    sitting_id = db.Column(db.ForeignKey('public.sitting.sitting_id'), nullable=False, index=True)
    sender = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    title = db.Column(db.Text)
    recipients = db.Column(db.Integer)

    sitting = db.relationship('Sitting', primaryjoin='Eminute.sitting_id == Sitting.sitting_id', backref='eminutes')


t_group_document_assignment = db.Table(
    'group_document_assignment',
    db.Column('group_id', db.ForeignKey('public.group.group_id'), primary_key=True, nullable=False),
    db.Column('doc_id', db.ForeignKey('public.doc.doc_id'), primary_key=True, nullable=False),
    schema='public'
)


class GroupMembershipRole(db.Model):
    __tablename__ = 'group_membership_role'
    __table_args__ = {'schema': 'public'}

    membership_id = db.Column(db.ForeignKey('public.user_group_membership.membership_id'), primary_key=True,
                              nullable=False)
    role_id = db.Column(db.String(256), primary_key=True, nullable=False)
    is_global = db.Column(db.Boolean)

    membership = db.relationship('UserGroupMembership',
                                 primaryjoin='GroupMembershipRole.membership_id == UserGroupMembership.membership_id',
                                 backref='group_membership_roles')


class Heading(db.Model):
    __tablename__ = 'heading'
    __table_args__ = {'schema': 'public'}

    heading_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    text = db.Column(db.String(512), nullable=False)
    status = db.Column(db.String(32))
    language = db.Column(db.String(5), nullable=False)
    group_id = db.Column(db.ForeignKey('public.group.group_id'))

    group = db.relationship('Group', primaryjoin='Heading.group_id == Group.group_id', backref='headings')


class Holiday(db.Model):
    __tablename__ = 'holiday'
    __table_args__ = {'schema': 'public'}

    holiday_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(1024))
    language = db.Column(db.String(5), nullable=False)


class ItemMemberVote(db.Model):
    __tablename__ = 'item_member_vote'
    __table_args__ = {'schema': 'public'}

    vote_id = db.Column(db.ForeignKey('public.item_vote.vote_id'), primary_key=True, nullable=False)
    member_id = db.Column(db.ForeignKey('public.user.user_id'), primary_key=True, nullable=False)
    vote = db.Column(db.Boolean)

    member = db.relationship('User', primaryjoin='ItemMemberVote.member_id == User.user_id',
                             backref='item_member_votes')
    vote1 = db.relationship('ItemVote', primaryjoin='ItemMemberVote.vote_id == ItemVote.vote_id',
                            backref='item_member_votes')


class ItemSchedule(db.Model):
    __tablename__ = 'item_schedule'
    __table_args__ = {'schema': 'public'}

    schedule_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    item_id = db.Column(db.Integer, nullable=False)
    item_type = db.Column(db.String(30), nullable=False)
    sitting_id = db.Column(db.ForeignKey('public.sitting.sitting_id'), nullable=False)
    planned_order = db.Column(db.Integer)
    real_order = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    item_status = db.Column(db.String(64))

    sitting = db.relationship('Sitting', primaryjoin='ItemSchedule.sitting_id == Sitting.sitting_id',
                              backref='item_schedules')


class ItemScheduleDiscussion(db.Model):
    __tablename__ = 'item_schedule_discussion'
    __table_args__ = {'schema': 'public'}

    discussion_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    schedule_id = db.Column(db.ForeignKey('public.item_schedule.schedule_id'))
    body = db.Column(db.Text)
    sitting_time = db.Column(db.Time)
    language = db.Column(db.String(5), nullable=False)

    schedule = db.relationship('ItemSchedule',
                               primaryjoin='ItemScheduleDiscussion.schedule_id == ItemSchedule.schedule_id',
                               backref='item_schedule_discussions')


class ItemScheduleVote(db.Model):
    __tablename__ = 'item_schedule_vote'
    __table_args__ = {'schema': 'public'}

    vote_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    schedule_id = db.Column(db.ForeignKey('public.item_schedule.schedule_id'))
    time = db.Column(db.Time)
    issue_item = db.Column(db.String(1024))
    issue_sub_item = db.Column(db.String(1024))
    document_uri = db.Column(db.String(1024))
    question = db.Column(db.String(1024))
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    result = db.Column(db.String(255))
    vote_type = db.Column(db.String(255))
    majority_type = db.Column(db.String(255))
    eligible_votes = db.Column(db.Integer)
    cast_votes = db.Column(db.Integer)
    votes_for = db.Column(db.Integer)
    votes_against = db.Column(db.Integer)
    votes_abstained = db.Column(db.Integer)
    roll_call = db.Column(db.String(32))
    mimetype = db.Column(db.String(127))
    language = db.Column(db.String(5), nullable=False)

    schedule = db.relationship('ItemSchedule', primaryjoin='ItemScheduleVote.schedule_id == ItemSchedule.schedule_id',
                               backref='item_schedule_votes')


class ItemVote(db.Model):
    __tablename__ = 'item_vote'
    __table_args__ = {'schema': 'public'}

    vote_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    item_id = db.Column(db.ForeignKey('public.doc.doc_id'), nullable=False)
    date = db.Column(db.Date)
    affirmative_vote = db.Column(db.Integer)
    negative_vote = db.Column(db.Integer)
    remarks = db.Column(db.Text)
    language = db.Column(db.String(5), nullable=False)

    item = db.relationship('Doc', primaryjoin='ItemVote.item_id == Doc.doc_id', backref='item_votes')


class MemberTitle(db.Model):
    __tablename__ = 'member_title'
    __table_args__ = (
        db.UniqueConstraint('membership_id', 'title_type_id'),
        {'schema': 'public'}
    )

    member_title_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    membership_id = db.Column(db.ForeignKey('public.user_group_membership.membership_id'), nullable=False)
    title_type_id = db.Column(db.ForeignKey('public.title_type.title_type_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    language = db.Column(db.String(5), nullable=False)

    membership = db.relationship('UserGroupMembership',
                                 primaryjoin='MemberTitle.membership_id == UserGroupMembership.membership_id',
                                 backref='member_titles')
    title_type = db.relationship('TitleType', primaryjoin='MemberTitle.title_type_id == TitleType.title_type_id',
                                 backref='member_titles')


class MinutesEmail(db.Model):
    __tablename__ = 'minutes_email'
    __table_args__ = {'schema': 'public'}

    minutes_email_id = db.Column(db.Integer, primary_key=True)
    sitting_id = db.Column(db.ForeignKey('public.sitting.sitting_id', ondelete='CASCADE'), nullable=False)
    sender = db.Column(db.Text)
    recipients = db.Column(db.Text)
    subject = db.Column(db.Text)
    message = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    sitting = db.relationship('Sitting', primaryjoin='MinutesEmail.sitting_id == Sitting.sitting_id',
                              backref='minutes_emails')


class OauthAccessToken(db.Model):
    __tablename__ = 'oauth_access_token'
    __table_args__ = {'schema': 'public'}

    access_token_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    authorization_token_id = db.Column(db.ForeignKey('public.oauth_authorization_token.authorization_token_id'),
                                       nullable=False)
    access_token = db.Column(db.String(100), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)

    authorization_token = db.relationship('OauthAuthorizationToken',
                                          primaryjoin='OauthAccessToken.authorization_token_id == OauthAuthorizationToken.authorization_token_id',
                                          backref='oauth_access_tokens')


class OauthApplication(db.Model):
    __tablename__ = 'oauth_application'
    __table_args__ = {'schema': 'public'}

    application_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    identifier = db.Column(db.Text, nullable=False, unique=True)
    name = db.Column(db.Text, nullable=False)
    secret = db.Column(db.String(100), nullable=False)
    redirection_endpoint = db.Column(db.Text, nullable=False)


class OauthAuthorization(db.Model):
    __tablename__ = 'oauth_authorization'
    __table_args__ = {'schema': 'public'}

    authorization_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_id = db.Column(db.ForeignKey('public.user.user_id'), nullable=False)
    application_id = db.Column(db.ForeignKey('public.oauth_application.application_id'), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    application = db.relationship('OauthApplication',
                                  primaryjoin='OauthAuthorization.application_id == OauthApplication.application_id',
                                  backref='oauth_authorizations')
    user = db.relationship('User', primaryjoin='OauthAuthorization.user_id == User.user_id',
                           backref='oauth_authorizations')


class OauthAuthorizationToken(db.Model):
    __tablename__ = 'oauth_authorization_token'
    __table_args__ = {'schema': 'public'}

    authorization_token_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    authorization_id = db.Column(db.ForeignKey('public.oauth_authorization.authorization_id'), nullable=False)
    authorization_code = db.Column(db.String(100), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    refresh_token = db.Column(db.String(100), nullable=False)

    authorization = db.relationship('OauthAuthorization',
                                    primaryjoin='OauthAuthorizationToken.authorization_id == OauthAuthorization.authorization_id',
                                    backref='oauth_authorization_tokens')


class Principal(db.Model):
    __tablename__ = 'principal'
    __table_args__ = {'schema': 'public'}

    principal_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), nullable=False)


class User(Principal):
    __tablename__ = 'user'
    __table_args__ = (
        db.CheckConstraint(
            "(active_p)::text = ANY (ARRAY[('A'::character varying)::text, ('I'::character varying)::text, ('D'::character varying)::text])"),
        db.CheckConstraint(
            "(gender)::text = ANY (ARRAY[('M'::character varying)::text, ('F'::character varying)::text])"),
        {'schema': 'public'}
    )

    user_id = db.Column(db.ForeignKey('public.principal.principal_id'), primary_key=True)
    login = db.Column(db.String(80), nullable=False, unique=True)
    salutation = db.Column(db.String(128))
    title = db.Column(db.String(128))
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    middle_name = db.Column(db.String(256))
    email = db.Column(db.String(512), nullable=False)
    gender = db.Column(db.String(1))
    date_of_birth = db.Column(db.Date)
    birth_country = db.Column(db.ForeignKey('public.country.country_id'))
    birth_nationality = db.Column(db.ForeignKey('public.country.country_id'))
    current_nationality = db.Column(db.ForeignKey('public.country.country_id'))
    marital_status = db.Column(db.String(128))
    uri = db.Column(db.String(1024), unique=True)
    date_of_death = db.Column(db.Date)
    type_of_id = db.Column(db.String(1))
    initials = db.Column(db.String(10))
    password = db.Column(db.String(36))
    salt = db.Column(db.String(24))
    description = db.Column(db.Text)
    remarks = db.Column(db.Text)
    image = db.Column(db.LargeBinary)
    active_p = db.Column(db.String(1))
    receive_notification = db.Column(db.Boolean)
    language = db.Column(db.String(5), nullable=False)

    country = db.relationship('Country', primaryjoin='User.birth_country == Country.country_id',
                              backref='country_country_users')
    country1 = db.relationship('Country', primaryjoin='User.birth_nationality == Country.country_id',
                               backref='country_country_users_0')
    country2 = db.relationship('Country', primaryjoin='User.current_nationality == Country.country_id',
                               backref='country_country_users')
    users = db.relationship(
        'User',
        secondary='public.user_delegation',
        primaryjoin='User.user_id == user_delegation.c.delegation_id',
        secondaryjoin='User.user_id == user_delegation.c.user_id',
        backref='users'
    )


class PasswordRestoreLink(User):
    __tablename__ = 'password_restore_link'
    __table_args__ = {'schema': 'public'}

    user_id = db.Column(db.ForeignKey('public.user.user_id'), primary_key=True)
    hash = db.Column(db.String(256), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)


class AdminUser(User):
    __tablename__ = 'admin_user'
    __table_args__ = {'schema': 'public'}

    user_id = db.Column(db.ForeignKey('public.user.user_id'), primary_key=True)


class Group(Principal):
    __tablename__ = 'group'
    __table_args__ = {'schema': 'public'}

    group_id = db.Column(db.ForeignKey('public.principal.principal_id'), primary_key=True)
    short_name = db.Column(db.String(512), nullable=False)
    full_name = db.Column(db.String(1024))
    acronym = db.Column(db.String(32))
    principal_name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.Text)
    status = db.Column(db.String(32))
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    sub_type = db.Column(db.String(128))
    parent_group_id = db.Column(db.ForeignKey('public.group.group_id'))
    language = db.Column(db.String(5), nullable=False)
    group_role = db.Column(db.String(256), nullable=False)
    cluster = db.Column(db.Text)
    prefix = db.Column(db.Text)
    custom3 = db.Column(db.Text)
    custom4 = db.Column(db.Text)

    parent_group = db.relationship('Group', remote_side=[group_id],
                                   primaryjoin='Group.parent_group_id == Group.group_id', backref='groups')


class Parliament(Group):
    __tablename__ = 'parliament'
    __table_args__ = {'schema': 'public'}

    parliament_id = db.Column(db.ForeignKey('public.group.group_id'), primary_key=True)
    parliament_type = db.Column(db.String(30))
    election_date = db.Column(db.Date, nullable=False)


class PoliticalGroup(Group):
    __tablename__ = 'political_group'
    __table_args__ = {'schema': 'public'}

    group_id = db.Column(db.ForeignKey('public.group.group_id'), primary_key=True)
    logo_data = db.Column(db.LargeBinary)
    logo_name = db.Column(db.String(127))
    logo_mimetype = db.Column(db.String(127))


class Committee(Group):
    __tablename__ = 'committee'
    __table_args__ = {'schema': 'public'}

    committee_id = db.Column(db.ForeignKey('public.group.group_id'), primary_key=True)
    group_continuity = db.Column(db.String(128), nullable=False)
    num_members = db.Column(db.Integer)
    min_num_members = db.Column(db.Integer)
    quorum = db.Column(db.Integer)
    num_clerks = db.Column(db.Integer)
    num_researchers = db.Column(db.Integer)
    proportional_representation = db.Column(db.Boolean)
    default_chairperson = db.Column(db.Boolean)
    reinstatement_date = db.Column(db.Date)


class Session(db.Model):
    __tablename__ = 'session'
    __table_args__ = {'schema': 'public'}

    session_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    parliament_id = db.Column(db.ForeignKey('public.parliament.parliament_id'), nullable=False)
    short_name = db.Column(db.String(512), nullable=False)
    full_name = db.Column(db.String(1024), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    language = db.Column(db.String(5), nullable=False)

    parliament = db.relationship('Parliament', primaryjoin='Session.parliament_id == Parliament.parliament_id',
                                 backref='sessions')


class Setting(db.Model):
    __tablename__ = 'setting'
    __table_args__ = {'schema': 'public'}

    setting_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    object_id = db.Column(db.Integer)
    object_type = db.Column(db.String(50))
    propertysheet = db.Column(db.String(50), index=True)
    name = db.Column(db.String(50))
    value = db.Column(db.String(400))
    type = db.Column(db.String(40))


class Signatory(db.Model):
    __tablename__ = 'signatory'
    __table_args__ = (
        db.UniqueConstraint('head_id', 'user_id'),
        {'schema': 'public'}
    )

    signatory_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    head_id = db.Column(db.ForeignKey('public.doc.doc_id'), nullable=False)
    user_id = db.Column(db.ForeignKey('public.user.user_id'), nullable=False)
    status = db.Column(db.String(32))

    head = db.relationship('Doc', primaryjoin='Signatory.head_id == Doc.doc_id', backref='signatories')
    user = db.relationship('User', primaryjoin='Signatory.user_id == User.user_id', backref='signatories')


class Sitting(db.Model):
    __tablename__ = 'sitting'
    __table_args__ = {'schema': 'public'}

    sitting_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    group_id = db.Column(db.ForeignKey('public.group.group_id'), nullable=False)
    session_id = db.Column(db.ForeignKey('public.session.session_id'))
    short_name = db.Column(db.String(512))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    sitting_length = db.Column(db.Integer)
    recurring_id = db.Column(db.Integer)
    recurring_type = db.Column(db.String(32))
    recurring_end_date = db.Column(db.DateTime)
    status = db.Column(db.String(48))
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    venue_id = db.Column(db.ForeignKey('public.venue.venue_id'))
    language = db.Column(db.String(5), nullable=False)
    activity_type = db.Column(db.String(1024))
    meeting_type = db.Column(db.String(1024))
    convocation_type = db.Column(db.String(1024))
    cancel_reason = db.Column(db.String(1024))

    group = db.relationship('Group', primaryjoin='Sitting.group_id == Group.group_id', backref='sittings')
    session = db.relationship('Session', primaryjoin='Sitting.session_id == Session.session_id', backref='sittings')
    venue = db.relationship('Venue', primaryjoin='Sitting.venue_id == Venue.venue_id', backref='sittings')


class SittingAgendaItem(db.Model):
    __tablename__ = 'sitting_agenda_item'
    __table_args__ = {'schema': 'public'}

    sitting_agenda_item_id = db.Column(db.Integer, primary_key=True)
    sitting_id = db.Column(db.ForeignKey('public.sitting.sitting_id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    status_date = db.Column(db.DateTime, nullable=False)

    sitting = db.relationship('Sitting', primaryjoin='SittingAgendaItem.sitting_id == Sitting.sitting_id',
                              backref='sitting_agenda_items')


class SittingAnalysisReport(db.Model):
    __tablename__ = 'sitting_analysis_report'
    __table_args__ = {'schema': 'public'}

    report_id = db.Column(db.Integer, primary_key=True)
    sitting_id = db.Column(db.ForeignKey('public.sitting.sitting_id', ondelete='CASCADE'), nullable=False)
    objective = db.Column(db.Text)
    outcome = db.Column(db.Text)
    analysis = db.Column(db.Text)
    atc_date = db.Column(db.DateTime)
    adoption_date = db.Column(db.DateTime)
    report_status = db.Column(db.Text)
    cost = db.Column(db.Numeric, server_default=db.FetchedValue())
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    sitting = db.relationship('Sitting', primaryjoin='SittingAnalysisReport.sitting_id == Sitting.sitting_id',
                              backref='sitting_analysis_reports')


class SittingAttendance(db.Model):
    __tablename__ = 'sitting_attendance'
    __table_args__ = {'schema': 'public'}

    sitting_id = db.Column(db.ForeignKey('public.sitting.sitting_id'), primary_key=True, nullable=False)
    member_id = db.Column(db.ForeignKey('public.user.user_id'), primary_key=True, nullable=False)
    attendance_type = db.Column(db.String(128), nullable=False)

    member = db.relationship('User', primaryjoin='SittingAttendance.member_id == User.user_id',
                             backref='sitting_attendances')
    sitting = db.relationship('Sitting', primaryjoin='SittingAttendance.sitting_id == Sitting.sitting_id',
                              backref='sitting_attendances')


t_sitting_audit = db.Table(
    'sitting_audit',
    db.Column('audit_id', db.Integer, nullable=False),
    db.Column('sitting_id', db.Integer, nullable=False),
    db.Column('group_id', db.Integer, nullable=False),
    db.Column('session_id', db.Integer),
    db.Column('short_name', db.String(512)),
    db.Column('start_date', db.DateTime, nullable=False),
    db.Column('end_date', db.DateTime, nullable=False),
    db.Column('sitting_length', db.Integer),
    db.Column('recurring_id', db.Integer),
    db.Column('recurring_type', db.String(32)),
    db.Column('recurring_end_date', db.DateTime),
    db.Column('status', db.String(48)),
    db.Column('status_date', db.DateTime, nullable=False, server_default=db.FetchedValue()),
    db.Column('venue_id', db.Integer),
    db.Column('language', db.String(5), nullable=False),
    db.Column('activity_type', db.String(1024)),
    db.Column('meeting_type', db.String(1024)),
    db.Column('convocation_type', db.String(1024)),
    db.Column('cancel_reason', db.String(1024)),
    schema='public'
)

t_sitting_report = db.Table(
    'sitting_report',
    db.Column('report_id', db.ForeignKey('public.doc.doc_id'), primary_key=True, nullable=False),
    db.Column('sitting_id', db.ForeignKey('public.sitting.sitting_id'), primary_key=True, nullable=False),
    schema='public'
)


class TimeBasedNotification(db.Model):
    __tablename__ = 'time_based_notification'
    __table_args__ = {'schema': 'public'}

    notification_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    object_id = db.Column(db.Integer, primary_key=True, nullable=False)
    object_type = db.Column(db.String(50), primary_key=True, nullable=False)
    object_status = db.Column(db.String(32))
    time_string = db.Column(db.String(50), primary_key=True, nullable=False)
    notification_date_time = db.Column(db.DateTime, nullable=False)


class TitleType(db.Model):
    __tablename__ = 'title_type'
    __table_args__ = {'schema': 'public'}

    title_type_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    group_id = db.Column(db.ForeignKey('public.group.group_id'), nullable=False)
    title_name = db.Column(db.String(80), nullable=False)
    user_unique = db.Column(db.Boolean)
    sort_order = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(5), nullable=False)

    group = db.relationship('Group', primaryjoin='TitleType.group_id == Group.group_id', backref='title_types')


class Translation(db.Model):
    __tablename__ = 'translation'
    __table_args__ = (
        db.Index('translation_lookup_index', 'object_id', 'object_type', 'lang'),
        {'schema': 'public'}
    )

    object_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    object_type = db.Column(db.String(50), primary_key=True, nullable=False)
    lang = db.Column(db.String(5), primary_key=True, nullable=False)
    field_name = db.Column(db.String(50), primary_key=True, nullable=False)
    field_text = db.Column(db.Text)


t_user_delegation = db.Table(
    'user_delegation',
    db.Column('user_id', db.ForeignKey('public.user.user_id'), primary_key=True, nullable=False),
    db.Column('delegation_id', db.ForeignKey('public.user.user_id'), primary_key=True, nullable=False),
    schema='public'
)

t_user_doc = db.Table(
    'user_doc',
    db.Column('user_id', db.ForeignKey('public.user.user_id'), primary_key=True, nullable=False),
    db.Column('doc_id', db.ForeignKey('public.doc.doc_id'), primary_key=True, nullable=False),
    schema='public'
)


class UserGroupMembership(db.Model):
    __tablename__ = 'user_group_membership'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'group_id'),
        {'schema': 'public'}
    )

    membership_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_id = db.Column(db.ForeignKey('public.user.user_id'), nullable=False)
    group_id = db.Column(db.ForeignKey('public.group.group_id'), nullable=False)
    status = db.Column(db.String(32))
    status_date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    active_p = db.Column(db.Boolean)
    replaced_id = db.Column(db.ForeignKey('public.user_group_membership.membership_id'), unique=True)
    substitution_type = db.Column(db.String(100))
    membership_type = db.Column(db.String(30), nullable=False)
    language = db.Column(db.String(5), nullable=False)

    group = db.relationship('Group', primaryjoin='UserGroupMembership.group_id == Group.group_id',
                            backref='user_group_memberships')
    replaced = db.relationship('UserGroupMembership', uselist=False, remote_side=[membership_id],
                               primaryjoin='UserGroupMembership.replaced_id == UserGroupMembership.membership_id',
                               backref='user_group_memberships')
    user = db.relationship('User', primaryjoin='UserGroupMembership.user_id == User.user_id',
                           backref='user_group_memberships')


class ParliamentMembership(UserGroupMembership):
    __tablename__ = 'parliament_membership'
    __table_args__ = {'schema': 'public'}

    membership_id = db.Column(db.ForeignKey('public.user_group_membership.membership_id'), primary_key=True)
    representation = db.Column(db.Text)
    party = db.Column(db.Text)
    member_election_type = db.Column(db.String(128), nullable=False)
    election_nomination_date = db.Column(db.Date)
    leave_reason = db.Column(db.String(40))


class Venue(db.Model):
    __tablename__ = 'venue'
    __table_args__ = {'schema': 'public'}

    venue_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    short_name = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text)
    language = db.Column(db.String(5), nullable=False)
    group_id = db.Column(db.ForeignKey('public.group.group_id'))

    group = db.relationship('Group', primaryjoin='Venue.group_id == Group.group_id', backref='venues')


class VpDatetime(db.Model):
    __tablename__ = 'vp_datetime'
    __table_args__ = {'schema': 'public'}

    object_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    object_type = db.Column(db.String(32), primary_key=True, nullable=False)
    name = db.Column(db.String(50), primary_key=True, nullable=False)
    value = db.Column(db.DateTime)


class VpText(db.Model):
    __tablename__ = 'vp_text'
    __table_args__ = {'schema': 'public'}

    object_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    object_type = db.Column(db.String(32), primary_key=True, nullable=False)
    name = db.Column(db.String(50), primary_key=True, nullable=False)
    value = db.Column(db.Text)


class VpTranslatedText(db.Model):
    __tablename__ = 'vp_translated_text'
    __table_args__ = {'schema': 'public'}

    object_id = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    object_type = db.Column(db.String(32), primary_key=True, nullable=False)
    name = db.Column(db.String(50), primary_key=True, nullable=False)
    value = db.Column(db.Text)
    language = db.Column(db.String(5), nullable=False)


t_zope_principal_role_map = db.Table(
    'zope_principal_role_map',
    db.Column('principal_id', db.String(50), nullable=False, index=True),
    db.Column('role_id', db.String(50), nullable=False),
    db.Column('setting', db.Boolean, nullable=False),
    db.Column('object_type', db.String(100)),
    db.Column('object_id', db.Integer),
    db.Index('prm_oid_idx', 'object_id', 'object_type'),
    schema='public'
)
