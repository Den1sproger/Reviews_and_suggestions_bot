from .db_work import Database


SQL_VIEW_REVIEWS = 'SELECT * FROM reviews;'
SQL_VIEW_SUGGESTIONS = 'SELECT * FROM suggestions;'
SQL_VIEW_MODERATING = 'SELECT * FROM moderation;'
SQL_VIEW_SUBSCRIBERS = 'SELECT chat_id FROM subscribers;'


def get_sql_add_review_to_db(review_text) -> str:
    return f'INSERT INTO reviews (review) VALUES ("{review_text}");'

def get_sql_add_suggestion_to_db(suggestion_text) -> str:
    return f'INSERT INTO suggestions (suggestion) VALUES ("{suggestion_text}");'

def get_sql_add_to_moderated(review_text) -> str:
    return f'INSERT INTO moderation (moderated_review) VALUES ("{review_text}");'

def get_sql_remove_from_moderated(review_text) -> str:
    return f'DELETE FROM moderation WHERE moderated_review = "{review_text}";'

def get_sql_remove_suggestion_from_db(suggestion_text) -> str:
    return f'DELETE FROM suggestions WHERE suggestion = "{suggestion_text}";'

def get_sql_remove_published_review(review_text) -> str:
    return f'DELETE FROM reviews WHERE review = "{review_text}";'


__all__ = [
    'Database',
    'SQL_VIEW_REVIEWS',
    'SQL_VIEW_SUGGESTIONS',
    'SQL_VIEW_MODERATING',
    'SQL_VIEW_SUBSCRIBERS',
    'get_sql_add_review_to_db',
    'get_sql_add_suggestion_to_db',
    'get_sql_add_to_moderated',
    'get_sql_remove_from_moderated',
    'get_sql_remove_suggestion_from_db',
    'get_sql_remove_published_review'
]