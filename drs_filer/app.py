"""Main app module."""

import logging

from foca import Foca

from drs_filer.ga4gh.drs.endpoints.service_info import RegisterServiceInfo

logger = logging.getLogger(__name__)


def main():
    foca = Foca("config.yaml")
    app = foca.create_app()

    # register service info
    with app.app.app_context():
        # FIXME: The line below is a hack, in order to support code written for
        # foca 0.6.0. To address it, update the code to refer to the foca
        # object via the syntax on the RHS.
        app.app.config['FOCA'] = app.app.config.foca
        service_info = RegisterServiceInfo()
        service_info.set_service_info_from_config()
    # start app
    app.run(port=app.port)


if __name__ == '__main__':
    main()
