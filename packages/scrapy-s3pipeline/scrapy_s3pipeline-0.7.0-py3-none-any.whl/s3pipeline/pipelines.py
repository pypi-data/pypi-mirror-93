from io import BytesIO
from urllib.parse import urlparse
from datetime import datetime
import gzip
from threading import Timer
import os.path

from scrapy.utils.misc import load_object

from s3pipeline.strategies.error import UploadError

class S3Pipeline:
    """
    Scrapy pipeline to store items into S3 bucket with JSONLines format.
    Unlike FeedExporter, the pipeline has the following features:

    * The pipeline stores items by chunk.
    * Support GZip compression.
    """

    def __init__(self, settings, stats):
        self.stats = stats

        url = settings['S3PIPELINE_URL']
        o = urlparse(url)
        self.bucket_name = o.hostname
        self.object_key_template = o.path[1:]  # Remove the first '/'

        self.max_chunk_size = settings.getint('S3PIPELINE_MAX_CHUNK_SIZE', 100)
        self.use_gzip = settings.getbool('S3PIPELINE_GZIP', url.endswith('.gz'))
        self.max_wait_upload_time = settings.getfloat('S3PIPELINE_MAX_WAIT_UPLOAD_TIME', 30.0)

        uncompressed_url = url[:-3] if url.endswith('.gz') else url
        _, ext = os.path.splitext(uncompressed_url)
        feed_exporter_key = ext[1:].lower()
        self.exporter_cls = load_object(settings.getwithbase('FEED_EXPORTERS').get(feed_exporter_key, 'scrapy.exporters.JsonLinesItemExporter'))

        if o.scheme == 's3':
            from .strategies.s3 import S3Strategy
            self.strategy = S3Strategy(settings)
        elif o.scheme == 'gs':
            from .strategies.gcs import GCSStrategy
            self.strategy = GCSStrategy(settings)
        else:
            raise ValueError('S3PIPELINE_URL must start with s3:// or gs://')

        self.items = []
        self.chunk_number = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler.stats)

    def process_item(self, item, spider):
        """
        Process single item. Add item to items and then upload to S3/GCS
        if size of items >= max_chunk_size.
        """
        self._timer_cancel()

        self.items.append(item)
        if len(self.items) >= self.max_chunk_size:
            self._upload_chunk()

        self._timer_start()

        return item

    def open_spider(self, spider):
        """
        Callback function when spider is open.
        """
        # Store timestamp to replace {time} in S3PIPELINE_URL
        self.ts = datetime.utcnow().replace(microsecond=0).isoformat().replace(':', '-')
        self._spider = spider
        self._timer = None

    def close_spider(self, spider):
        """
        Callback function when spider is closed.
        """
        # Upload remained items to S3.
        self._upload_chunk()
        self._timer_cancel()

    def _upload_chunk(self):
        """
        Do upload items to S3/GCS.
        """

        if not self.items:
            return  # Do nothing when items is empty.

        f = self._make_fileobj()

        # Build object key by replacing variables in object key template.
        object_key = self.object_key_template.format(**self._get_uri_params())

        try:
            self.strategy.upload_fileobj(f, self.bucket_name, object_key)
        except UploadError:
            self.stats.inc_value('pipeline/s3/fail')
            raise
        else:
            self.stats.inc_value('pipeline/s3/success')
        finally:
            # Prepare for the next chunk
            self.chunk_number += len(self.items)
            self.items = []

    def _get_uri_params(self):
        params = {}
        for key in dir(self._spider):
            params[key] = getattr(self._spider, key)

        params['chunk'] = self.chunk_number
        params['time'] = self.ts
        return params

    def _make_fileobj(self):
        """
        Build file object from items.
        """

        bio = BytesIO()
        f = gzip.GzipFile(mode='wb', fileobj=bio) if self.use_gzip else bio

        # Build file object using ItemExporter
        exporter = self.exporter_cls(f, encoding='utf-8')
        exporter.start_exporting()
        for item in self.items:
            exporter.export_item(item)
        exporter.finish_exporting()

        if f is not bio:
            f.close()  # Close the file if GzipFile

        # Seek to the top of file to be read later
        bio.seek(0)

        return bio

    def _timer_start(self):
        """
        Start the timer in s3pipeline
        """
        self._timer = Timer(self.max_wait_upload_time, self._upload_chunk)
        self._timer.start()

    def _timer_cancel(self):
        """
        Stop the timer in s3pipeline
        """
        if self._timer is not None:
            self._timer.cancel()
