# coding=utf-8
import logging

from flask import request
from flask_restplus import Namespace, Resource

from diglett.base.beanret import BeanRet
from diglett.base.file_tool import FileTool
from diglett.rest.endpoints.serializers import bean

"""
this is main process of python file exec on OS,
it will create file and change file content,it can running it
stop it.

1.create python file and stop running
2.run python file and return result
3.init project from further
4.rename a file and folder
5.write code to file
6.read file content to webide frontend
7.delete file and folder ,if there some files and sub folders delete all of them
"""

log = logging.getLogger(__name__)
ns_file = Namespace(name='file', description='Describes the operations related with the teams')


@ns_file.route("/rename/")
@ns_file.param('oldPath', 'The path like  /xx/xx/xx.py')
@ns_file.param('newPath', 'The path like  /xx/xx/xx.py')
class Rename(Resource):
    @ns_file.marshal_with(bean)
    def put(self):
        """
        rename the old path to the new path,if it is a file just rename the file name,
        but if it is a folder and has some sub folders, it will iterate all of them and
        move them to the folder
        :return:
        """
        old_path = request.args.get("oldPath")
        new_path = request.args.get("newPath")
        if not old_path or not new_path:
            return BeanRet(success=False)
        file_tool = FileTool()
        root_path = file_tool.workspace()
        list = file_tool.rename(root_path, old_path, new_path)
        return BeanRet(True, data=list)


@ns_file.route("/")
@ns_file.param('path', 'The path like  /xx/xx/xx.py')
@ns_file.param('content', 'the file content')
class CodeFile(Resource):
    @ns_file.marshal_with(bean)
    def put(self):
        """
        create & write the content to the file
        :return:
        """
        path = request.args.get("path")
        content = request.args.get('content')
        if not path or not content:
            return BeanRet(success=False)

        file_tool = FileTool()
        file_path = file_tool.workspace(path)
        file_tool.write(file_path, content)
        return BeanRet(success=True)

    @ns_file.marshal_with(bean)
    def get(self):
        """
        read python file content
        :return:  content
        """
        path = request.args.get("path")
        if not path:
            return BeanRet(success=False)

        file_tool = FileTool()
        file_path = file_tool.workspace(path)
        content = file_tool.read(file_path)

        if content:
            return BeanRet(success=True, data={"content": content})
        else:
            return BeanRet(success=False)

    @ns_file.marshal_with(bean)
    def delete(self):
        """
        remove file
        :return: True
        """
        path = request.args.get("path")
        if not path:
            return BeanRet(success=False)

        file_tool = FileTool()
        file_path = file_tool.workspace(path)
        file_tool.remove(file_path)
        return BeanRet(success=True, data=path)
