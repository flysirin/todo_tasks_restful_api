from flask import jsonify, make_response
import logging
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError, IntegrityError, \
    DatabaseError, DataError, InternalError, NotSupportedError, InterfaceError

logging.basicConfig(level=logging.ERROR)
logger_db_error = logging.getLogger(__name__)


def handle_sqlalchemy_error(error: SQLAlchemyError):
    e = str(error.__dict__["orig"])
    logger_db_error.error(f"{e}")
    return make_response(jsonify({'message': f'Database error'}), 500)


def handle_programming_error(error: ProgrammingError):
    logger_db_error.error(f"{error.orig}")
    return make_response(jsonify({'message': f'Database error'}), 500)


def handle_integrity_error(error: IntegrityError):
    logger_db_error.error(f"{error.orig}")
    return make_response(jsonify({'message': f'Database error'}), 500)


def handle_database_error(error: DatabaseError):
    logger_db_error.error(f"{error.orig}")
    return make_response(jsonify({'message': f'Database error'}), 500)


def handle_data_error(error: DataError):
    logger_db_error.error(f"{error.orig}")
    return make_response(jsonify({'message': f'Database error: {error.orig}'}), 500)


def handle_internal_error(error: InternalError):
    logger_db_error.error(f"{error.orig}")
    return make_response(jsonify({'message': f'Database error'}), 500)


def handle_not_supported_error(error: NotSupportedError):
    logger_db_error.error(f"{error.orig}")
    return make_response(jsonify({'message': f'Database error'}), 500)


def handle_interface_error(error: InterfaceError):
    logger_db_error.error(f"{error.orig}")
    return make_response(jsonify({'message': f'Database error: '}), 500)


def register_error_handlers(app):
    app.register_error_handler(DataError, handle_data_error)
    app.register_error_handler(ProgrammingError, handle_programming_error)
    app.register_error_handler(SQLAlchemyError, handle_sqlalchemy_error)
    app.register_error_handler(IntegrityError, handle_integrity_error)
    app.register_error_handler(DatabaseError, handle_database_error)
    app.register_error_handler(InternalError, handle_internal_error)
    app.register_error_handler(NotSupportedError, handle_not_supported_error)
    app.register_error_handler(InterfaceError, handle_interface_error)
