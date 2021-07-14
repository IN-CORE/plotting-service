import cachedb
import connexion
from connexion.resolver import RestyResolver

def create_app(test_config=None):
    # if debug:
    #     logging.basicConfig(
    #         format='%(asctime)-15s %(message)s', level=logging.DEBUG)
    # else:
    #     logging.basicConfig(
    #         format='%(asctime)-15s %(message)s', level=logging.INFO)


    options = {"swagger_ui": False}
    app = connexion.FlaskApp(__name__.split('.')[0])
    app.add_api('plotting-service-api.yaml', 
            resolver=RestyResolver("api"), 
            resolver_error=501,
            options=options)
    flask_app = app.app

    if test_config is None:
        flask_app.config.from_pyfile('config.py', silent=True)
    else:
        flask_app.config.from_mapping(test_config)
    
    flask_app.teardown_appcontext(cachedb.close_db)

    return flask_app

app = create_app()

if __name__ == "__main__":
    debug = True
    app.run(port=5000, debug=debug)
# testing fragility (old) 5b47b2d7337d4a36187c61c9
# testing new fragility 5f6ccf67de7b566bb71b202d
