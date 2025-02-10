"""Theme configuration for the GUI."""

THEME = {
    'PRIMARY_COLOR': '#2B2D42',
    'SECONDARY_COLOR': '#8D99AE',
    'ACCENT_COLOR': '#EF233C',
    'BACKGROUND_COLOR': '#EDF2F4',
    'TEXT_COLOR': '#2B2D42',
    'ERROR_COLOR': '#D90429',
    'SUCCESS_COLOR': '#4CAF50',
    'WARNING_COLOR': '#FFC107',
    'INFO_COLOR': '#2196F3',
}

DARK_THEME = {
    'PRIMARY_COLOR': '#EDF2F4',
    'SECONDARY_COLOR': '#8D99AE',
    'ACCENT_COLOR': '#EF233C',
    'BACKGROUND_COLOR': '#2B2D42',
    'TEXT_COLOR': '#EDF2F4',
    'ERROR_COLOR': '#D90429',
    'SUCCESS_COLOR': '#4CAF50',
    'WARNING_COLOR': '#FFC107',
    'INFO_COLOR': '#2196F3',
}

def get_theme(dark_mode=False):
    """Get the current theme configuration."""
    return DARK_THEME if dark_mode else THEME
