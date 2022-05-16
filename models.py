from sqlalchemy.schema import UniqueConstraint

from dashboard import db


class Component(db.Model):
    '''
    Component component ID
    '''
    id = db.Column(db.Integer, primary_key=True)


class Rating(db.Model):
    '''
    Rating ID --> named rating mapping
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    component = db.Column(
        'component_id',
        db.Integer,
        db.ForeignKey('component.id'),
        nullable=False)


# Should be able to access entities list (backref)
#
class TableColumn(db.Model):
    __tablename__ = 'tablecolumn'

    name = db.Column(db.String, primary_key=True)


# Should be able to access entities (backref)
class TableRow(db.Model):
    __tablename__ = 'tablerow'

    name = db.Column(db.String, primary_key=True)


class Entity(db.Model):
    '''
    Single entity to QC
    '''
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # columnname
    # columnname_id
    columnname = db.Column(
        'columnname_id',
        db.ForeignKey('tablecolumn.name'),
        nullable=False)
    rowname = db.Column(
        'rowname_id',
        db.ForeignKey('tablerow.name'),
        nullable=False)
    # component
    # component_id
    component = db.Column(
        'component_id',
        db.Integer,
        db.ForeignKey('component.id'),
        nullable=False)
    comment = db.Column(db.Text, default="")
    failed = db.Column(db.Boolean)
    # rating
    # rating_id
    rating = db.Column('rating_id', db.ForeignKey('rating.id'))

    @property
    def has_failed(self):
        if self.failed is True:
            return "Fail"
        elif self.failed is False:
            return "Pass"
        else:
            return ""

    @property
    def entry(self):
        if self.rating:
            rating = self.rating.name
        else:
            rating = ""
        return (
            rating,
            self.has_failed,
            self.comment or ""
        )


class Image(db.Model):
    '''
    Images used for an Entity to assess quality
    '''
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text)
    # # entity
    # # entity_id
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'))

    __table_args__ = (UniqueConstraint(path), )


# This is defined to make it easier to dynamically change databases
# for the models at runtime
tables = [Component, Rating, TableColumn, TableRow, Entity, Image]
