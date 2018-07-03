import falcon

import lib.helpers as helpers
import lib.security as security

class Me(object):
    @helpers.authorize
    def on_get(self, req, resp, user_id):
        try:
            resp.body = helpers.to_json(security.get_user(user_id))
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_404)