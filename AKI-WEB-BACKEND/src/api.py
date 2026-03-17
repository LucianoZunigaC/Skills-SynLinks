from fastapi import APIRouter, Security

from .features.auth.endpoints import protected_router as protected_auth_router
from .features.auth.endpoints import public_router as public_auth_router
from .features.forms.endpoints import router as forms_router
from .features.groups.endpoints import router as groups_router
from .features.packages.endpoints import router as packages_router
from .features.packages_files.endpoints import router as packages_files_router
from .features.pandas.endpoints import router as pandas_router
from .features.users.endpoints import protected_router as protected_users_router
from .features.users.endpoints import public_router as public_users_router
from .shared.security import oauth2_scheme

api_prefix= "/api/v1"

# WARNING: Don't use this unless you want unauthenticated routes
protected_api_router = APIRouter(dependencies=[Security(oauth2_scheme)])
# WARNING: Don't use this unless you want unauthenticated routes
public_api_router = APIRouter()

protected_api_router.include_router(groups_router,
                                    prefix=api_prefix + "/groups",
                                    tags=["Groups"])

protected_api_router.include_router(packages_router,
                                    prefix=api_prefix + "/packages",
                                    tags=["Packages"])

protected_api_router.include_router(packages_files_router,
                                    prefix=api_prefix + "/packages",
                                    tags=["Packages"])

protected_api_router.include_router(forms_router,
                                    prefix=api_prefix + "/forms",
                                    tags=["Forms"])

protected_api_router.include_router(pandas_router,
                                    prefix=api_prefix + "/pandas",
                                    tags=["Pandas"])

protected_api_router.include_router(protected_users_router,
                                    prefix=api_prefix + "/users",
                                    tags=["Users"])


public_api_router.include_router(public_users_router,
                                 prefix=api_prefix + "/users",
                                 tags=["Users"])

protected_api_router.include_router(protected_auth_router, prefix=api_prefix + "/auth", tags=["OAuth 2.0"])
public_api_router.include_router(public_auth_router, prefix=api_prefix + "/auth", tags=["OAuth 2.0"])
