from .apps import QuizConfig as quiz_config


def quiz(request):
    return {
        'QUIZ_TICKET_URL': quiz_config.QUIZ_TICKET_URL,
    }
