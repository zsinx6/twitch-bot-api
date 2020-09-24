from bot_api.models import User


def test_a_transaction(db_session):
    row = db_session.query(User).get(1)
    row.username = "testing"
