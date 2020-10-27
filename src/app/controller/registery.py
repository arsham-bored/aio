from flask import Request

class Registery:

    class Options:
        @staticmethod
        def to_boolean(state: str):
            return True if state == 'on' else False

        def __init__(self, request: Request):
            self.cloth = self.to_boolean(request.form.get('cloth', None))
            self.plate = self.to_boolean(request.form.get('plate', None))
            self.leather = self.to_boolean(request.form.get('leather', None))
            self.mail = self.to_boolean(request.form.get('mail', None))

    @staticmethod
    def form_is_empty(request: Request):
        return request.form.to_dict() == {}

    def register_user(self, request: Request):
        realm = request.form.get("realm", None)
        roles = request.form.get("roles", None)
        userid = request.form.get("userid", None)
        apply = request.form.get("apply", None)
        raider = request.form.get("raider", None)
        warcraft = request.form.get("warcraft", None)
        options = self.Options(request)

        return "done."