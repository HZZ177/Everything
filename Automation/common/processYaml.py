import yaml
from common.configLog import logger
import os
from common import filepath


class Yaml:
    def __init__(self, filename, mode):
        """
        filename 文件名
        mode 模式：1 统一平台地址 2 收费系统6.0管理后台地址 3 6.x收费web 4 直接拿host 5 后付费系统 6 bi系统 7 easytest平台 8 永策pro
        """
        self.filename = filename
        self.mode = mode

    def read_yaml(self):
        """获取yaml中数据"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    file_data = f.read()
                data = yaml.load(file_data, Loader=yaml.FullLoader)
                return data
            except Exception as msg:
                raise Exception(logger.error(msg))
        else:
            raise FileNotFoundError(logger.error("没有找到文件:%s" % self.filename))

    def _get_domain(self):
        """获取域名"""
        try:
            domain_dict = {
                1: filepath.config.get("roadTollSystem").get("domain"),
                2: filepath.config.get("app").get("domain"),
                3: filepath.config.get("hardware_platform").get("domain"),
                4: filepath.config.get("client").get("domain"),
                5: filepath.config.get("yongcePro").get("domain"),
                99: self.read_yaml().get("host"),
                0: ""
            }
            if self.mode not in domain_dict.keys():
                raise Exception(logger.error("mode参数输入错误"))
            domain = domain_dict.get(self.mode)
            return domain
        except Exception as msg:
            raise Exception(logger.error(msg))

    @property
    def url(self):
        """
        获取api
        return url:str
        """
        domian = self._get_domain()
        try:
            data = self.read_yaml()["api"]
            return "".join((domian, data))
        except KeyError as msg:
            raise KeyError(logger.error("KeyError:{%s}" % msg))

    @property
    def method(self):
        """
        获取method
        return url:str

        """
        try:
            data = self.read_yaml()["method"]
            return data
        except KeyError as msg:
            raise KeyError(logger.error("KeyError:{%s}" % msg))

    @property
    def headers(self):
        """
        获取headers
        return dict
        """
        try:
            headers = self.read_yaml()['headers'] if self.read_yaml()['headers'] else {}
            return headers
        except KeyError as msg:
            raise KeyError(logger.error("KeyError:{%s}" % msg))

    @property
    def allData(self):
        """
        获取data数据
        return list --> [[{ps}, {data}], [{ps}, {data}] ...]
        """
        try:
            allData = self.read_yaml()['data']
            return allData
        except KeyError as msg:
            raise KeyError(logger.error("KeyError:{%s}" % msg))

    @property
    def title(self):
        """
        获取title数据
        return list --> [[{ps}, {data}], [{ps}, {data}] ...]
        """
        try:
            title = self.read_yaml()['title']
            return title
        except KeyError as msg:
            raise KeyError(logger.error("KeyError:{%s}" % msg))

    @property
    def allQuery(self):
        """
        获取query数据
        return list --> [[{ps}, {query}], [{ps}, {query}] ...]
        """
        try:
            allQuery = self.read_yaml()['query']
            return allQuery
        except KeyError as msg:
            raise KeyError(logger.error("KeyError:{%s}" % msg))

    @property
    def allDb(self):
        """
        获取相关db数据
        :return:
        """
        try:
            allDb = self.read_yaml()['db']
            return allDb
        except KeyError as msg:
            raise KeyError(logger.error("KeyError:{%s}" % msg))


if __name__ == "__main__":
    read_data = Yaml(filepath.USERINFOBYMMS, 4)
    print(read_data.read_yaml())
    # allData = read_data.allData
    # for data in allData:
    #     print(data[0]['id'])
    #     print(data[0]['id'] == 1)
    #     print(data[1]['ps'])
    #     print(data[2])