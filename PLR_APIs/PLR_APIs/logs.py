import logging

logging.basicConfig(filename="debug/debug.log",
                    format='''%(asctime)s %(name)-15s %(levelname)-5s %(message)s : 
                              [%(pathname)s line %(lineno)d, in %(funcName)s ]''',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)