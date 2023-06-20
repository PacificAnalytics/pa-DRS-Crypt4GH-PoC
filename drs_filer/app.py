"""Main app module."""

import logging

from foca import Foca

from drs_filer.ga4gh.drs.endpoints.service_info import RegisterServiceInfo
from drs_filer.crypt4gh_support.config import Crypt4GHConfig

logger = logging.getLogger(__name__)


def main():
    foca = Foca("config.yaml")
    foca.conf.crypt4gh = Crypt4GHConfig(**foca.conf.crypt4gh)

    app = foca.create_app()

    # register service info
    with app.app.app_context():
        service_info = RegisterServiceInfo()
        service_info.set_service_info_from_config()
    # start app
    app.run(port=app.port)


if __name__ == '__main__':
    main()
