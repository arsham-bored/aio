from quart import Request
from quart import (
    render_template,
    redirect,
    url_for
)
from ...orm.models.user import User
from ...orm.engine import session
from ..utility import RaiderScrapper

class Registery:

    class Option:
        @staticmethod
        def to_boolean(state: str):
            return True if state == 'on' else False

    class Armor(Option):
        def __init__(self, request: Request, form):

            self.cloth = self.to_boolean(form.get('cloth', False))
            self.plate = self.to_boolean(form.get('plate', False))
            self.leather = self.to_boolean(form.get('leather', False))
            self.mail = self.to_boolean(form.get('mail', False))


    class Apply(Option):
        def __init__(self, request: Request, form):
            
            self.raider = self.to_boolean(form.get('raider', False))
            self.m = self.to_boolean(form.get('m', False))


    async def register_user(self, request: Request):
        form = await request.form

        try:
            print(form)

            realm = form.get("realm", "")
            roles = form.get("roles", "")
            userid = form.get("userid", None)
            raider = form.get("raider-link", None)
            warcraft = form.get("warcraft", "")
            referer = form.get("referer", "")
            info = form.get("info", "")
            armor = self.Armor(request, form)
            apply = self.Apply(request, form)

            scraper = RaiderScrapper(raider)
            data = await scraper.get_content()
            parser = scraper.parse(data)

            raider_name = parser.name
            raider_score = parser.score

            username, user_id = realm.split("-")

            query = session.query(User).filter(
                User.username == username
            ).all()

            print(query)

            if not len(query) == 0:
                print("yes")
                return redirect(url_for("registery.fail"))

            print(raider_name, username)
            print(raider_name == username)

            if raider_name.lower() == username.lower():
                
                print("tes")

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
                
                if raider_score is not None:
                    raider_score = raider_score.replace(",", "")
                    raider_score = float(raider_score)

                    user.score = raider_score

                else:
                    user.score = 0

                # save to database
                session.add(user)
                session.commit()

                return redirect(url_for("registery.success"))

            return redirect(url_for("registery.fail"))

        except Exception as error:
            print(error)
            return redirect(url_for("registery.fail"))

        

