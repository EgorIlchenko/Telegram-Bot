from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

from config_data.config import DATE_FORMAT, DB_PATH


db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField()


class History(BaseModel):
    history_id = AutoField()
    user = ForeignKeyField(User, backref='histories')
    name = CharField(null=True)
    year = CharField(null=True)
    ageRating = IntegerField(null=True)
    genres = CharField(null=True)
    rating = IntegerField(null=True)
    description = CharField(null=True)
    poster = CharField(null=True)
    is_viewed = BooleanField(default=False)
    due_date = DateField(null=True)

    def __str__(self):
        return ("*{name} ({year}), {ageRating}+*\n{tab}\nЖанр: {genres}\n"
                "Рейтинг на Кинопоиске: {rating}\nСюжет: {description}\n".format(
            date=self.due_date,
            name=self.name,
            year=self.year,
            ageRating=self.ageRating,
            tab='-'*40,
            genres=self.genres,
            rating=self.rating,
            description=self.description
        ))


def create_models():
    db.create_tables(BaseModel.__subclasses__())
