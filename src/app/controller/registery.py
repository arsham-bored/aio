from flask import Request
from flask import (
    render_template,
    redirect,
    url_for
)
from ...orm.models.user import User
from ...orm.engine import session

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
        print(request.form)
        print(request.form.to_dict())
        print(len(request.form.to_dict()))
        return len(request.form.to_dict()) < 3

    def register_user(self, request: Request):
        realm = request.form.get("realm", None)
        roles = request.form.get("roles", None)
        userid = request.form.get("userid", None)
        raider = request.form.get("raider", None)
        warcraft = request.form.get("warcraft", None)
        referer = request.form.get("referer", "")
        info = request.form.get("info", "")
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
        session.add(user)
        session.commit()
        print(user)

        print(
            session.query(User).filter(
                User.username == userid
            ).all()
        )

        return redirect(url_for("registery.success"))

        

