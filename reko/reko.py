from reko.cachestore import CacheStore
from reko.cameraman import CameraMan
from reko.rekognition import Rekognition


class Reko(object):
    def __init__(self, profile, collection_id):
        self.collection_id = collection_id
        self._cameraman = CameraMan()
        self._cache = CacheStore()
        self._rekognition = Rekognition(profile)

    def __del__(self):
        pass

    def list_collections(self):
        """
        List all collections.
        """
        return self._rekognition.list_collections()

    def list_faces(self):
        """
        List all faces of the current collection.
        """
        return self._rekognition.list_faces(collection_id=self.collection_id)

    def signin(self, id=None):
        """
        :param id: (optional) external_image_id
        :return: external_image_id or None if not found
        """
        if not self._rekognition.collection_exist(collection_id=self.collection_id):
            return None

        # Take an image
        if self.take_picture() is False:
            return None

        try:
            ret_id = self._rekognition.search_faces_by_image(
                collection_id=self.collection_id, image_file=self._cache.cache_img, external_image_id=id)
        except Exception as e:
            print(e.message)
            return None

        return ret_id

    def signup(self, id):
        """
        :param id: external_image_id
        :return:
        """
        if not self._rekognition.collection_exist(collection_id=self.collection_id) \
                and not self._rekognition.create_collection(collection_id=self.collection_id):
            return False

        # Take an image
        if self.take_picture() is False:
            return False

        # Store face
        succeeded = self._rekognition.index_faces(
            collection_id=self.collection_id, image_file=self._cache.cache_img, external_image_id=id)

        return succeeded

    def take_picture(self):
        """
        Connect to the webcam and capture an image and save to the give file.
        """
        # Take an image
        return self._cameraman.take_picture(image_name=self._cache.cache_img)

    def delete_collection(self):
        """
        Delete the current collection.
        """
        return self._rekognition.delete_collection(collection_id=self.collection_id)
