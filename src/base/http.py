from urllib import request, parse

from src import logger
from src.base.beanret import BeanRet


def get(url):
    logger.info(url)
    response = request.urlopen(url)
    result = response.read().decode(encoding='utf-8')
    logger.info(result)
    if result != None:
        beanret = BeanRet()
        beanret.to_obj(result)
        return beanret


def post(url, data=None):
    try:
        logger.info(url)
        postdata = parse.urlencode(data).encode('utf-8')
        req = request.Request(url, data=postdata, method="POST")
        response = request.urlopen(req)
        result = response.read().decode(encoding='utf-8')
        logger.info(result)
        beanret = BeanRet().to_obj(result)
        return beanret
    except:
        return BeanRet(success=False)
