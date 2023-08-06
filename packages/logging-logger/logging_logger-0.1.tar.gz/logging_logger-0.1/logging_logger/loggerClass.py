import logging

class loggerClass:

    def WriteLog(logger,level,message):
        if level==logging.INFO:
                logger.info(message)

        elif level==logging.DEBUG:
                logger.debug(message)

        elif level==logging.CRITICAL:
                logger.critical(message)

        elif level==logging.WARNING:
                logger.warning(message)

        elif level==logging.ERROR:
                logger.error(message)
            

    def WritetoScreen(self,level, message,format):
        
        #logging.basicConfig(level=level,format=format)
        logger1 = logging.getLogger(__name__)
        logger1.setLevel(level)

        stream_handler= logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(format))
        logger1.addHandler(stream_handler)

        self.WriteLog(logger1,level,message)

    def Writetofile(self,file_name, level, message,format='%(asctime)s:%(levelname)s:%(message)s'):
        logger = logging.getLogger(__name__)
        logger.setLevel(level)
        
        formatter = logging.Formatter(format)
        
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        self.WriteLog(logger,level,message)

        
        
    

