import logging
import logging.config

logging.config.fileConfig('logging.conf')
logging.getLogger('imdbpy').setLevel(logging.WARNING)
logging.getLogger('imdb').setLevel(logging.WARNING)
log = logging.getLogger(__name__)
