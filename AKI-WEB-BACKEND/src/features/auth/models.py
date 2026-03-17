from sqlalchemy import Column, Integer, String, DateTime

from src.core import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    loginId = Column(String(320), nullable=False, unique=True)
    email = Column(String(320), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    lastName = Column(String(100), nullable=False)
    userType = Column(String(30), nullable=False)
    hashedPassword = Column(String, nullable=False)
    status = Column(String(1), nullable=False)
    xd_creation = Column(DateTime, nullable=False)
    xd_creationUser = Column(String(100), nullable=False)
    xd_lastUpdate = Column(DateTime, nullable=False)
    xd_lastUpdateUsr = Column(String(100), nullable=False)

#
# class Role(Base):
#     __tablename__ = 'roles'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#     users = relationship("User", back_populates="role")
#     permissions = relationship("RolePermission", back_populates="role")
#
#
# class Permission(Base):
#     __tablename__ = 'permissions'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#
#
# class RolePermission(Base):
#     __tablename__ = 'role_permissions'
#
#     role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
#     permission_id = Column(Integer, ForeignKey('permissions.id'), primary_key=True)
#     role = relationship("Role", back_populates="permissions")
#     permission = relationship("Permission")
