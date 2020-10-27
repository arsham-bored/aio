from flask import Request
from ...orm.models.user import User


class Registery:

    class Option:
        @staticmethod
        def to_boolean(state: str):
            return True if state == 'on' else False

    class Armor(Option):
        def __init__(self, request: Request):
            self.cloth = self.to_boolean(request.form.get('cloth', None))
            self.plate = self.to_boolean(request.form.get('plate', None))
            self.leather = self.to_boolean(request.form.get('leather', None))
            self.mail = self.to_boolean(request.form.get('mail', None))


    class Apply(Option):
        def __init__(self, request: Request):
            self.raider = self.to_boolean(request.form.get('raider', False))
            self.m = self.to_boolean(request.form.get('m', False))


    @staticmethod
    def form_is_empty(request: Request):
        return request.form.to_dict() == {}

    def register_user(self, request: Request):
        realm = request.form.get("realm", None)
        roles = request.form.get("roles", None)
        userid = request.form.get("userid", None)
        raider = request.form.get("raider", None)
        warcraft = request.form.get("warcraft", None)
        armor = self.Armor(request)
        apply = self.Apply(request)
        

        user = User()

        user.realm = realm
        user.role = roles
        user.username = userid
        
        return "got data."

        

