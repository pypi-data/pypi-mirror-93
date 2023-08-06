#!/usr/bin/python
import sys
import os
import time
import pandas as pd
from sqlalchemy import create_engine
import datetime
from colorama import init
from termcolor import cprint
from argparse import ArgumentParser
from pyfiglet import figlet_format
from hurry.filesize import size, alternative
import logging as log
log.basicConfig(level=log.NOTSET, format="[%(levelname)s] %(message)s")


class Dumper(object):
    def __init__(self, args):
        self.start_time = time.time()
        log.debug('start timepoch: {}'.format(self.start_time))
        self._big_file = args.file
        self._file_buffer = args.buffer
        self._table = args.table
        self._max = args.max

        # get database engine
        self._dbengine = self.__get_mysql_engine(
            database_name=args.database,
            user=args.user,
            password=args.password,
            host=args.host,
            port=args.port
        )

        # start pushing
        self.pushtomysql()

    @staticmethod
    def __is_file_exist(file_path):
        if not os.path.isfile(file_path):
            raise FileExistsError('{} file not found'.format(file_path))

    @staticmethod
    def __get_mysql_engine(database_name, user, password, host, port):
        log.debug('creating database engine...')
        engine = create_engine(
            "mysql://{}:{}@{}:{}/{}".format(
                user,
                password,
                host,
                port,
                database_name
            ),
            echo=True
        )
        return engine

    def pushtomysql(self):
        '''
        push to mysql
        '''

        # check file is exist
        try:
            self.__is_file_exist(self._big_file)
        except FileExistsError as ex:
            log.error(ex)

        # calculate file size
        file_size = os.path.getsize(self._big_file)
        redable_file_size = size(file_size, system=alternative)
        log.debug('total file size in byte: {}'.format(file_size))
        log.info('total fle size in redable format: {}'.format(redable_file_size))
        log.info('readig file with buffer size: {}'.format(self._file_buffer))

        # create database engine
        engine = self._dbengine

        try:
            # open file
            with open(self._big_file, buffering=int(self._file_buffer), mode="rb",) as f:
                df = pd.read_excel(f.read())
            f.close()

            # push to sql
            df.to_sql(self._table, engine, if_exists='replace')
        except Exception as ex:
            log.error("{} {}".format(type(ex).__name__, ex))

        # calculate script execution time
        end_time = time.time()
        total_time = str(datetime.timedelta(
            seconds=end_time - self.start_time))

        log.debug(
            'total time taken by script in format (H:MM:SS.ms): {}'.format(total_time))


def main():
    # banner
    print("\n")
    init(strip=not sys.stdout.isatty())
    fig_font = 'cricket'
    cprint(figlet_format("MySQL Sheet", font=fig_font),
           'red', attrs=['bold'])
    print("[!] MySQL Sheet.\n\n")

    # arguments
    argparse = ArgumentParser(description='dump big xlsheet in mysql table')
    argparse.add_argument(
        '-f', '--file', help='big xlsheet file path', required=True)
    argparse.add_argument(
        '-b', '--buffer', help='file buffuer in bytes default buffer size is 4096', default=4096)
    argparse.add_argument(
        '-u', '--user', help='mysql username default user is root', default='root')
    argparse.add_argument('-p', '--password',
                          help='mysql password default is empty', default='')
    argparse.add_argument(
        '--host', help='mysql hostname default is localhost', default='localhost')
    argparse.add_argument('--port', help='database port number', default=3306)
    argparse.add_argument('-d', '--database',
                          help='mysql database name', required=True)
    argparse.add_argument(
        '-t', '--table', help='mysql table name', required=True)
    argparse.add_argument(
        '-m', '--max', help='max record push concurrently in msyql')
    args = argparse.parse_args()

    # call main function
    Dumper(args)
