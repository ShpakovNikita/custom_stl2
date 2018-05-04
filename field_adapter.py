import json
import collections
import os
from field import Field as FieldGame
from peewee import *


Status = collections.namedtuple('status', ['in_game', 'ready'])
stat = Status(in_game=0, ready=1)


db_filename = 'data.db'
new_db_flag = not os.path.exists(db_filename)
db = SqliteDatabase(db_filename)


class Player(Model):
    status = SmallIntegerField()

    class Meta:
        database = db



class Field(Model):
    player_one = ForeignKeyField(Player, related_name='player_one')
    player_zero = ForeignKeyField(Player, related_name='player_zero')

    json_field = TextField()
    win_param = IntegerField()
    current_player = SmallIntegerField()

    class Meta:
        database = db


class Request(Model):
    sender = ForeignKeyField(Player, related_name='sender')
    receiver = ForeignKeyField(Player, related_name='receiver')
    established = BooleanField(default=False)

    class Meta:
        database = db


def get_last_id():
    # This function gets last id to add task on it's place

    query = Player.select().order_by(Player.id.desc())

    try:
        return query.get().id

    except DoesNotExist:
        return 1


def start_session():
    # returns uid of new player
    player = Player.create(status=stat.ready)
    return player.id


def end_session(uid):
    # delete uid from queue
    try:
        Player.delete().where(Player.id == uid).execute()
        Request.delete().where((Request.sender == uid) |
                               (Request.receiver == uid)).execute()
        Field.delete().where((Field.player_one == uid) |
                             (Field.player_zero == uid)).execute()
    except DoesNotExist:
        raise ValueError('Error during the session\'s ending!')


def send_request(sender, receiver):

    player_1 = Player.select().where(Player.id == sender)
    player_2 = Player.select().where(Player.id == receiver)

    if _check_other_request(sender, receiver):
        Request.create(sender=player_1.get(), receiver=player_2.get(),
                       established=True)
        con = Request.select().where((Request.sender == receiver) &
                                     (Request.receiver == sender)).get()
        con.established = True
        con.save()
        print('Request accepted!')
        return

    try:
        if player_1.get().id == player_2.get().id:
            print('You cannot request to yourself!')
            return


        try:
            Request.select().where((Request.sender == sender) &
                                   (Request.receiver == receiver)).get()
            print('You are already send request to that player')
            return
        except:
            pass

        Request.create(sender=player_1.get(), receiver=player_2.get())
        print('Request send!')

    except:
        return


def _check_other_request(sender, receiver):
    try:
        Request.select().where((Request.sender == receiver) &
                               (Request.receiver == sender)).get()
        return True
    except:
        return False


def print_field(uid):
    try:
        fin = Field.select().where((Field.player_one == uid) |
                                   (Field.player_zero == uid)).get()
        game = FieldGame(1)
        game.load_field(fin.json_field,
                        fin.win_param,
                        fin.current_player)
        game.print()
    except:
        print('Player left the game!')


def make_turn(cell, player, uid):
    try:
        fin = Field.select().where((Field.player_one == uid) |
                                   (Field.player_zero == uid)).get()
        game = FieldGame(1)
        game.load_field(fin.json_field,
                        fin.win_param,
                        fin.current_player)

        if player[0] != fin.current_player:
            print('Wait for the opponent\'s turn')

        else:
            try:
                game.make_turn(cell)
                if game.is_win():
                    print('Game over')

                if fin.json_field != game.return_field_json():
                    fin.current_player ^= 1
                    fin.json_field = game.return_field_json()
                    fin.save()

            except ValueError:
                pass

    except:
        print('Player left the game!')


def check_for_connection(uid, player):
    try:
        uid_query = Request.select().where(Request.sender == uid)

        for q in uid_query:
            if q.established == True:
                try:
                    fin = Field.select().where((Field.player_one == uid) |
                                         (Field.player_zero == uid)).get().id
                    player[0] = 0
                    return fin
                except:
                    game = FieldGame(3)
                    port = Field.create(player_one=q.sender,
                                        player_zero=q.receiver,
                                        json_field=game.return_field_json(),
                                        win_param=game._size_to_win,
                                        current_player=1)
                    player[0] = 1
                    return port.id

        return False

    except:
        return False


def see_players():
    print('STATUS: 1 - ready, 0 - in game')
    for player in Player.select():
        print('pid: {}, STATUS: {}'.format(player.id, player.status))


def see_requests(uid):
    for request in Request.select().where(Request.receiver == uid):
        print('pid: %s' % request.sender.id)

def change_status():
    pass


def _run():
    Player.create_table()
    Field.create_table()
    Request.create_table()


if new_db_flag:
    _run()