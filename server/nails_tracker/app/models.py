import textwrap

from server.nails_tracker.app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(320), index=True, unique=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    # role = db.Column(db.Enum)
    info = db.Column(db.Text)

    salon_creator_salons = db.relationship(
        'Salon',
        foreign_keys='Salon.creator_id',  # ???
        backref='creator',
        lazy='dynamic'
    )
    salon_admin_salons = db.relationship(
        'Salon',
        secondary='salon_admin_salon',
        backref=db.backref('salon_admins', lazy='dynamic'),
        lazy='dynamic'
    )
    master_salons = db.relationship(
        'Salon',
        secondary='master_salon',
        backref=db.backref('masters', lazy='dynamic'),
        lazy='dynamic'
    )

    textures = db.relationship('Texture', backref='master', lazy='dynamic')

    client_events = db.relationship(
        'Event',
        foreign_keys='Event.client_id',
        backref='client',
        lazy='dynamic'
    )
    master_events = db.relationship(
        'Event',
        foreign_keys='Event.master_id',
        backref='master',
        lazy='dynamic'
    )

    def __repr__(self):
        return textwrap.dedent(f'''
        <User(
            id={self.id};
            login={self.login};
            email={self.email};
            full_name={self.full_name}
        )>
        ''').strip()


class Salon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    info = db.Column(db.Text)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    events = db.relationship('Event', backref='salon', lazy='dynamic')

    def __repr__(self):
        return textwrap.dedent(f'''
        <Salon(
            id={self.id};
            name={self.name};
            creator={self.creator}
        )>
        ''').strip()


salon_admin_salon = db.Table(
    'salon_admin_salon',
    db.Column(
        'salon_admin_id',
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True
    ),
    db.Column(
        'salon_id',
        db.Integer,
        db.ForeignKey('salon.id'),
        primary_key=True
    )
)

master_salon = db.Table(
    'master_salon',
    db.Column(
        'master_id',
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True
    ),
    db.Column(
        'salon_id',
        db.Integer,
        db.ForeignKey('salon.id'),
        primary_key=True
    )
)


class Texture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    info = db.Column(db.String(255))
    file = db.Column(db.Text, nullable=False)

    master_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return textwrap.dedent(f'''
        <Texture(
            id={self.id};
            name={self.name};
            info={self.info};
            master={self.master}
        )>
        ''').strip()


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, index=True, nullable=False)
    info = db.Column(db.Text)

    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    master_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'))

    def __repr__(self):
        return textwrap.dedent(f'''
        <Event(
            id={self.id};
            datetime={self.datetime};
            client={self.client};
            master={self.master};
            salon={self.salon}
        )>
        ''').strip()
