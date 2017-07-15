# -*- coding: utf-8 -*-
import ConfigParser
import os
import sys

from saltfish.utils.parsers import OptionParser
from saltfish.modules import service
from saltfish.utils.exceptions import ServiceError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
class CreateNodejsServiceOptionPares(OptionParser):
    description = 'Create Nodejs Service'
    usage = 'aaa'
    description = 'bbb'
    optionals_title = ''
    positionals_title = 'ddd'
    def _set_arguments(self):
        self.description = '%s --project p2p  --appname bigtwo --startid 10 --endid 10 --interval 2' % self.prog
        self.add_argument('--project', metavar='ProjectName', action='store')
        self.add_argument('--appname', metavar='AppName')
        self.add_argument('--startid', metavar='Number', type=int, default=0, help='specify service ID,default is 0')
        self.add_argument('--endid', metavar='Number', type=int, default=0, help='specify service ID,default is 0')
        self.add_argument('--interval', metavar='Number', type=int, default=1, help='specify service ID interval,default is 1')
        self.add_argument('-f', '--file', help='Specify the configuration file')
        self.add_argument('--cover', action='store_true', help='Whether it is covered')


class CreateService(object):
    options = {
        'template': None,
        'template_dir': None,
        'name_rule': None,
        'service_dir': None,
        'suffix': None
    }
    def __init__(self, project, appname, startid=0, endid=0, interval=0, file=None, cover=False, *args, **kwargs):
        self.set_options(project.upper(), file)
        id_list = [int(startid), int(endid) + 1, int(interval)]
        self.options['ProjectName'] = project.upper()
        self.options['AppName'] = appname.upper()
        self.options['id_list'] = id_list
        self.options['cover'] = cover
        super(CreateService, self).__init__()

    def set_options(self, section, file=None):
        if not file:
            file = 'saltfish/config/service.conf'
        c = ConfigParser.ConfigParser()
        c.read(file)
        if c.has_section(section):
            for i in self.options:
                self.options[i] = c.get(section, i)

        else:
            msg = '在配置文件中没有找到项目[%s]' % section
            raise ServiceError(msg)

    def generate_name(self, **kwargs):
        name = self.options['name_rule'].format(**kwargs)
        return name

    def generate_args(self):
        _kwargs = {}
        if self.options['id_list'] != [0, 1, 0]:
            for i in range(*self.options['id_list']):
                _kwargs['name'] = self.generate_name(ID=i, **self.options)
                _kwargs['ID'] = i
                _kwargs['file'] = os.path.join(self.options['service_dir'], _kwargs['name'] + '.' + self.options['suffix'])
                yield dict(_kwargs, **self.options)
        else:
            _kwargs['name'] = self.generate_name(**self.options)
            _kwargs['file'] = os.path.join(self.options['service_dir'], _kwargs['name'] + '.' + self.options['suffix'])
            yield dict(_kwargs, **self.options)


    def run(self):
        for i in self.generate_args():
            print i['file']
            connext = service.render(**i)
            service.write(connext=connext, file=i['file'])

class TaskMQ(CreateService):
    options = {
        'template': None,
        'template_dir': None,
        'name_rule': None,
        'service_dir': None,
        'suffix': None,
        'project_path': None
    }
    def generate_args(self):
        s_list_file = os.path.join()


def nodejs(*args, **kwargs):
    s = CreateService(*args, **kwargs)
    s.run()

a=CreateNodejsServiceOptionPares()
a.parse_args('--project p2p  --appname bigtwo --startid 10 --endid 10'.split())
nodejs(**a.config)