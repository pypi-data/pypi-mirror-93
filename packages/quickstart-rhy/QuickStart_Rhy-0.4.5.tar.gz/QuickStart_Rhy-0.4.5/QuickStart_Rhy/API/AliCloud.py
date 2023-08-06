# coding=utf-8
"""
阿里云相关API

Alibaba cloud API
"""
from . import pre_check, user_lang, dir_char
try:
    import oss2
except ImportError:
    exit('You need to install "oss2"')


class AliyunOSS:
    def __init__(self, ac_id=pre_check('aliyun_oss_acid'), ac_key=pre_check('aliyun_oss_ackey'),
                 bucket_url=pre_check('aliyun_oss_bucket_url'), df_bucket=pre_check('aliyun_oss_df_bucket')):
        """
        初始化并登陆阿里云对象存储

        Initializes and logs into ali cloud object storage

        :param ac_id: Access id
        :param ac_key: Access key
        :param bucket_url: oss-[地区 | location].aliyuncs.com
        :param df_bucket: 桶名称
        """
        self.ac_id = ac_id
        self.ac_key = ac_key
        self.bucket_url = bucket_url
        self.df_bucket = df_bucket
        self.auth = oss2.Auth(self.ac_id, self.ac_key)

    def get_func_table(self):
        """
        获取OSS类支持的操作

        Get the operations supported by the OSS class

        :return: 支持的函数字典
        """
        return {
            '-up': self.upload,
            '-rm': self.remove,
            '-dl': self.download,
            '-ls': self.list_bucket
        }

    def upload(self, filePath: str, bucket: str = None):
        """
        上传文件（支持断点续传）

        Upload file (support breakpoint continuation)

        :param filePath: 文件路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        filePath = filePath.strip()
        oss2.resumable_upload(bucket, filePath.replace(dir_char, '/'), filePath, num_threads=4)

    def download(self, filename: str, bucket: str = None):
        """
        下载文件（支持断点续传）

        Download file (support breakpoint continuation)

        :param filename: 文件在bucket中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        oss2.resumable_download(bucket, filename, filename, num_threads=4)

    def remove(self, filePath: str, bucket: str = None):
        """
        删除文件

        delete file

        :param filePath: 文件在bucket中的路径
        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        bucket = bucket if bucket else self.df_bucket
        bucket = oss2.Bucket(self.auth, self.bucket_url, bucket)
        bucket.delete_object(filePath)

    def list_bucket(self, bucket: str = None):
        """
        打印桶中的文件表

        Print the file table in the bucket

        :param bucket: 桶名称，缺省使用self.df_bucket
        :return: None
        """
        from .. import qs_default_console, qs_info_string
        from ..NetTools.NormalDL import size_format
        from rich.table import Table, Column
        from rich.text import Text
        from rich.box import SIMPLE
        bucket = bucket if bucket else self.df_bucket
        ls = oss2.Bucket(self.auth, self.bucket_url, bucket)
        tb = Table(
            *([Column('File', justify="center"), Column('Size', justify="center")]
              if user_lang != 'zh' else
              [Column('文件', justify="center"), Column('体积', justify="center")])
            , show_edge=False, row_styles=['none', 'dim'], box=SIMPLE, title='[bold underline]Aliyun OSS'
        )
        prefix = dict()
        for obj in oss2.ObjectIterator(ls):
            if '/' in obj.key:
                prefix[obj.key[obj.key[:obj.key.index('/')]]] = 0
            tb.add_row(Text(obj.key, justify='left'), Text(size_format(obj.size, True), justify='right'))
        qs_default_console.print(
            qs_info_string,
            'Bucket Url:' if user_lang != 'zh' else '桶链接:',
            'https://' + bucket + '.' + self.bucket_url + '/'
        )
        qs_default_console.print(tb, justify="center")
