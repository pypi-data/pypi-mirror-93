from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship

from .orm import get_base


Base = get_base()


class Account(Base):
    """
    Модель "Учетная запись"
    """
    __tablename__ = 'accounts'

    # Идентификатор
    id = Column(Integer, primary_key=True)

    # Наименование
    name = Column(String)

    def __repr__(self):
        return '<Account {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return self.name


class Wiki(Base):
    """
    Модель "Wiki"
    """
    __tablename__ = 'wikis'

    # Идентификатор
    id = Column(Integer, primary_key=True)

    # Заголовок
    title = Column(String(255))

    def __repr__(self):
        return '<Wiki {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return self.title


class EnrollmentTerm(Base):
    """
    Модель "EnrollmentTerm"
    """
    __tablename__ = 'enrollment_terms'

    # Идентификатор
    id = Column(Integer, primary_key=True)

    # Корневая учетная запись
    root_account_id = Column(ForeignKey('accounts.id'))
    root_account = relationship('Account')

    # Наименование
    name = Column(String(255))

    def __repr__(self):
        return '<EnrollmentTerm {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return self.name


class SisBatch(Base):
    """
    Модель "SisBatch"
    """
    __tablename__ = 'sis_batches'

    # Идентификатор
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return '<SisBatch {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return self.id


class Course(Base):
    """
    Модель "Курс"
    """
    __tablename__ = 'courses'

    # Идентификатор
    id = Column(Integer, primary_key=True)

    # Наименование курса
    name = Column(String(255))

    # Учетная запись
    account_id = Column(ForeignKey('accounts.id'))
    account = relationship('Account')

    group_weighting_scheme = Column(String(255))

    # Статус
    workflow_state = Column(String(255))

    # Уникальный идентификатор
    uuid = Column(String(255))

    start_at = Column(DateTime)

    conclude_at = Column(DateTime)

    grading_standard_id = Column(Integer)

    # Публичный
    is_public = Column(Boolean)

    allow_student_wiki_edits = Column(Boolean)

    # Дата и время создания
    created_at = Column(DateTime)

    # Дата и время изменения
    updated_at = Column(DateTime)

    show_public_context_messages = Column(Boolean)

    syllabus_body = Column(String)

    allow_student_forum_attachments = Column(Boolean)

    default_wiki_editing_roles = Column(String(255))

    # Wiki
    wiki_id = Column(ForeignKey('wikis.id'))
    wiki = relationship('Wiki')

    allow_student_organized_groups = Column(Boolean)

    # Код курса
    course_code = Column(String(255))

    # Вид по-умолчанию
    default_view = Column(String(255))

    abstract_course_id = Column(Integer)

    # Корневая учетная запись
    root_account_id = Column(ForeignKey('accounts.id'))
    root_account = relationship('Account')

    enrollment_term_id = Column(ForeignKey('enrollment_terms.id'))
    enrollment_term = relationship('EnrollmentTerm')

    # SIS-идентификатор
    sis_source_id = Column(String(255))

    sis_batch_id = Column(ForeignKey('sis_batches.id'))
    sis_batch = relationship('SisBatch')

    open_enrollment = Column(Boolean)

    storage_quota = Column(Integer)

    tab_configuration = Column(String)

    # Разрешить комментарии к Wiki
    allow_wiki_comments = Column(Boolean)

    turnitin_comments = Column(String)

    self_enrollment = Column(Boolean)

    # Лицензия
    license = Column(String(255))

    indexed = Column(Boolean)

    restrict_enrollments_to_course_dates = Column(Boolean)

    template_course_id = Column(Integer)

    # Локализация
    locale = Column(String(255))

    # Настройки курса
    settings = Column(String)

    replacement_course_id = Column(Integer)

    stuck_sis_fields = Column(String)

    # Публичное описание
    public_description = Column(String)

    self_enrollment_code = Column(String(255))

    self_enrollment_limit = Column(Integer)

    integration_id = Column(String(255))

    # Временная зона
    time_zone = Column(String(255))

    lti_context_id = Column(String(255))

    turnitin_id = Column(Integer)

    show_announcements_on_home_page = Column(Boolean)

    home_page_announcement_limit = Column(Integer)

    latest_outcome_import_id = Column(Integer)

    grade_passback_setting = Column(String(255))


    def __repr__(self):
        return '<Course {} (id={}, sis_source_id={})>'.format(self, self.id, self.sis_source_id)
    
    def __str__(self):
        return self.name


class CourseSection(Base):
    """
    Модель "Секция курса"
    """

    __tablename__ = 'course_sections'

    id = Column(Integer, primary_key=True)
    sis_source_id = Column(String(255))
    course_id = Column(ForeignKey('courses.id'))
    course = relationship('Course')
    name = Column(String(255))
    workflow_state = Column(String(255))

    def __repr__(self):
        return '<CourseSection {} (id={}, sis_source_id={})>'.format(self, self.id, self.sis_source_id)
    
    def __str__(self):
        return self.name


class ContextModule(Base):
    """
    Модель "Модули курса"
    """

    __tablename__ = 'context_modules'

    id = Column(Integer, primary_key=True)
    context_id = Column(Integer)
    context_type = Column(String(255))
    name = Column(String)
    position = Column(Integer)
    workflow_state = Column(String(255))

    def __repr__(self):
        return '<ContextModule {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return self.name


class ContentTag(Base):
    __tablename__ = 'content_tags'

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer)
    content_type = Column(String(255))
    title = Column(String)
    context_module_id = Column(ForeignKey('context_modules.id'))
    context_module = relationship('ContextModule')
    workflow_state = Column(String(255))

    def __repr__(self):
        return '<ContentTag {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return self.title


class Score(Base):
    """
    Модель "Оценки"
    """

    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True)
    enrollment_id = Column(ForeignKey('enrollments.id'))
    workflow_state = Column(String(255))
    current_score = Column(Float)
    final_score = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return '<Score {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return self.current_score


class Submission(Base):
    """
    Модель "Отправленные работы"
    """

    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True)
    score = Column(Float)
    assignment_id = Column(ForeignKey('assignments.id'))
    assignment = relationship('Assignment')
    user_id = Column(ForeignKey('users.id'))
    user = relationship('User')
    workflow_state = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __repr__(self):
        return '<Submission {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return str(self.score)


class Assignment(Base):
    """
    Модель "Задание"
    """

    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    submission_types = Column(String(255))
    workflow_state = Column(String(255))

    def __repr__(self):
        return '<Assignment {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return self.title


class Override(Base):
    """
    Модель "Назначение"
    """
    __tablename__ = 'assignment_overrides'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    assignment_id = Column(ForeignKey('assignments.id'))
    assignment = relationship('Assignment')
    assignment_version = Column(Integer)
    set_type = Column(String)
    set_id = Column(Integer)
    title = Column(String)
    workflow_state = Column(String)
    due_at_overridden = Column(Boolean)
    due_at = Column(DateTime)
    all_day = Column(Boolean)
    all_day_date = Column(DateTime)
    unlock_at_overridden = Column(Boolean)
    unlock_at = Column(DateTime)
    lock_at_overridden = Column(Boolean)
    lock_at = Column(DateTime)
    quiz_id = Column(ForeignKey('quizzes.id'))
    quiz = relationship('Quiz')
    quiz_version = Column(Integer)

    def __repr__(self):
        return '<Override {} (id={} assignment_id={} workflow_state={} quiz_id={})>'.format(self, self.id, self.assignment_id, self.workflow_state, self.quiz_id)
    
    def __str__(self):
        return self.title


class OverrideStudent(Base):
    """
    Модель "Студент в Назначении"
    """
    __tablename__ = 'assignment_override_students'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    assignment_id = Column(ForeignKey('assignments.id'))
    assignment = relationship('Assignment')
    override_id = Column('assignment_override_id', ForeignKey('assignment_overrides.id'))
    override = relationship('Override')
    user_id = Column(ForeignKey('users.id'))
    user = relationship('User')
    quiz_id = Column(ForeignKey('quizzes.id'))
    quiz = relationship('Quiz')
    workflow_state = Column(String)

    def __repr__(self):
        return '<OverrideStudent {} (id={} assignment_id={} override_id={} user_id={} quiz_id={} workflow_state={}>'.format(self, self.id, self.assignment_id, self.override_id, self.user_id, self.quiz_id, self.workflow_state)
    
    def __str__(self):
        return str(self.user)


class User(Base):
    """
    Модель "Пользователь"
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def __repr__(self):
        return '<User {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return self.name


class Pseudonym(Base):
    """
    Модель "Псевдонимы"
    """

    __tablename__ = 'pseudonyms'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'))
    user = relationship('User')
    position = Column(Integer)
    sis_user_id = Column(String(255))

    def __repr__(self):
        return '<Pseudonym {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return str(self.user)


class Quiz(Base):
    """
    Модель "Тест"
    """

    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    assignment_id = Column(ForeignKey('assignments.id'))
    assignment = relationship('Assignment')

    def __repr__(self):
        return '<Quiz {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return self.name


class Enrollment(Base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'))
    user = relationship('User')
    course_id = Column(ForeignKey('courses.id'))
    course = relationship('Course')
    type = Column(String(255))
    course_section_id = Column(ForeignKey('course_sections.id'))
    course_section = relationship('CourseSection')
    workflow_state = Column(String(255))
    sis_pseudonym_id = Column(ForeignKey('pseudonyms.id'))
    sis_pseudonym = relationship('Pseudonym')

    def __repr__(self):
        return '<Enrollment {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return str(self.user)