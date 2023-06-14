from .static import (check_review_ikb,
                     check_suggestion_ikb,
                     general_menu_kb,
                     get_admin_menu_kb)
from .dynamic import (get_admin_moderation_ikb,
                      get_admin_suggestions_ikb, 
                      get_reviews_ikb)


__all__ = [
    'check_review_ikb',
    'check_suggestion_ikb',
    'get_admin_moderation_ikb',
    'get_admin_suggestions_ikb',
    'get_reviews_ikb',
    'general_menu_kb',
    'get_admin_menu_kb'
]