from flask import Request
from ...orm.models.user import User


class Registery:

    class Option:
        @staticmethod
        def to_boolean(state: str):
            return True if state == 'on' else False

    class Armor(Option):
        def __init__(self, request: Request):
            self.cloth = self.to_boolean(request.form.get('cloth', False))
            self.plate = self.to_boolean(request.form.get('plate', False))
            self.leather = self.to_boolean(request.form.get('leather', False))
            self.mail = self.to_boolean(request.form.get('mail', False))


    class Apply(Option):
        def __init__(self, request: Request):
            self.raider = self.to_boolean(request.form.get('raider', False))
            self.m = self.to_boolean(request.form.get('m', False))


    @staticmethod
    def form_is_empty(request: Request):
        return len(request.form.to_dict()) < 4

    def register_user(self, request: Request):
        realm = request.form.get("realm", None)
        roles = request.form.get("roles", None)
        userid = request.form.get("userid", None)
        raider = request.form.get("raider", None)
        warcraft = request.form.get("warcraft", None)
        referer = request.form.get("referer", None)
        info = request.form.get("info", None)
        armor = self.Armor(request)
        apply = self.Apply(request)
        

        user = User()

        user.username = userid
        user.realm = realm
        user.role = roles
        user.raider_link = raider
        user.warcraft = warcraft
        user.referer = referer
        user.info = info

        user.is_m = apply.m
        user.is_raider = apply.raider
        user.is_cloth = armor.cloth
        user.is_leather = armor.leather
        user.is_plate = armor.plate
        user.is_mail = armor.mail
        
        # save to database

        return "got data."

        

