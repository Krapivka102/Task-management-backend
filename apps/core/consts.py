class TaskStatus:
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    CLOSED = 'closed'

    CHOICES = ((OPEN, 'Открыта'), (IN_PROGRESS, 'В процессе'), (CLOSED, 'Завершена'))


class TaskPriority:
    LOW = 'open'
    MEDIUM = 'in_progress'
    HIGH = 'closed'

    CHOICES = ((LOW, 'Низкий'), (MEDIUM, 'Средний'), (HIGH, 'Высокий'))


class MembershipRole:
    VIEWER = 'viewer'
    DEVELOPER = 'developer'
    MAINTAINER = 'maintainer'

    CHOICES = (
        (VIEWER, 'зритель'),
        (DEVELOPER, 'разработчик'),
        (MAINTAINER, 'ответственный'),
    )
