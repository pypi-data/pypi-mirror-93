import sys
import requests
import logging
from s3.client import Client

PAGE_NUMBER_MAX = 1e6


def process_json(data, entity):
    """
    update data after retrieving from s3
    Args:
        data: row data json
    Returns: list
    """
    if entity in ("leads", "companies", "contacts", "tasks"):
        items = [item for item in data["_embedded"]["items"]]
    elif entity in "funnels":
        items = [item for key, item in data["_embedded"]["items"].items()]
    elif entity in "users":
        items = [item for key, item in data["_embedded"]["users"].items()]
    return items


class AmocrmApiLoader:
    """
    CLASS LOADER from API TO S3, v2 https://www.amocrm.com/developers/content/digital_pipeline/site_visit/
    """

    def __init__(
            self,
            entity,
            s3_path,
            args_s3,
            args_api,
            date_modified_from=None,
            with_offset=True,
            batch_api=500,
    ):
        """
        :param entity:   amocrm entities contacts/users/accounts e.t.c
        :param s3_path:  path for s3 where is files should be uploaded
        :param args_s3:  dict with aws_access_key_id/aws_secret_access_key/endpoint_url=None/bucket=None
        :param args_api: dict with AMO_USER_LOGIN/AMO_USER_HASH/AMO_AUTH_URL keys required
        :param date_modified_from: date update we loading data
        :param with_offset:
        :param batch_api: size of batch to upload
        """
        log_format = "%(asctime)-15s %(name)s:%(levelname)s: %(message)s"
        logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)
        logging.basicConfig(format=log_format, stream=sys.stderr, level=logging.ERROR)
        logging.captureWarnings(True)
        self.logger = logging.getLogger(__class__.__name__)

        self.entity = entity

        self.args_api = args_api
        self.batch_api = batch_api
        self.date_modified_from = date_modified_from
        self.with_offset = with_offset
        self.rows_to_upload = 0

        self.s3_path = s3_path

        if self.__auth():
            self.s3_client = Client(**args_s3)
            if not self.s3_client.path_exists(self.s3_path):
                self.s3_client.create_dir(self.s3_path)

    def __auth(self):
        """API authorization"""
        params = {
            "USER_LOGIN": self.args_api["AMO_USER_LOGIN"],
            "USER_HASH": self.args_api["AMO_USER_HASH"],
            "type": "json",
        }
        r = requests.post(self.args_api["AMO_AUTH_URL"], data=params)
        response = r.json()

        if response["response"]["auth"]:
            self.auth_cookie_str = r.cookies
            self.logger.info(
                "AmoCRM: Authorized user {user}".format(
                    user=self.args_api["AMO_AUTH_URL"]
                )
            )
            return True
        else:
            self.logger.info(response["response"])
            raise ValueError("AmoCRM: Not authorized")
            return False

    def clear_s3_folder(self):
        if self.s3_client.path_exists(self.s3_path):
            for file in self.s3_client.get_file_list(self.s3_path):
                self.logger.info("Delete {file} from s3".format(file=file))
                self.s3_client.delete_file(path=file)
            self.s3_client.delete_dir(self.s3_path)  # remove directory

    def __get_file_name(self, offset, batch):
        """
        Returns: s3 file name
        """
        return "{dir_path}/{entity}_{offset}_{batch}.json".format(
            dir_path=self.s3_path, entity=self.entity, offset=offset, batch=batch
        )

    def extract(self):
        """load table from api"""
        self.clear_s3_folder()  # clear old before loading
        headers = {
            "Content-Type": "application/json",
        }
        url_base = self.args_api["amocrm_api_url"]
        cur_offset = 0
        count_uploaded = self.batch_api

        params = {}
        while cur_offset < PAGE_NUMBER_MAX and count_uploaded == self.batch_api:
            file_path = self.__get_file_name(cur_offset, self.batch_api)
            self.logger.info("Extracting page number {}".format(cur_offset))
            if self.date_modified_from is not None:
                self.logger.info("Uploading data with after {}".format(self.date_modified_from))
                url = url_base.format(batch_size_api=self.batch_api, offset=cur_offset)
                headers["IF-MODIFIED-SINCE"] = self.date_modified_from.strftime(
                    "%a, %d %b %Y %H:%M:%S UTC"
                )
            else:
                url = url_base
            self.logger.info(url)
            objects = requests.get(
                url, cookies=self.auth_cookie_str, headers=headers, params=params
            )
            try:
                count_uploaded = len(process_json(objects.json(), self.entity))
                self.logger.info(
                    "Saving data in file {}, count rows {}, total: {}".format(
                        file_path, count_uploaded, self.rows_to_upload
                    )
                )
                self.s3_client.create_file(file_path, objects.content)
                self.rows_to_upload += count_uploaded
            except Exception as e:
                self.logger.info("Can't load objects.content, exception: {e}".format(e=e))
                self.logger.info(
                    "Objects.content: {content}".format(content=objects.content)
                )
                exit(0)
            cur_offset += self.batch_api
        self.logger.info("Total number of rows received from API is {}".format(self.rows_to_upload))
