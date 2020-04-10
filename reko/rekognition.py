import boto3

DEFAULTS = {
    "region_name": "ap-southeast-2"  # Sydney
}


def status_code(ret):
    return ret["ResponseMetadata"]["HTTPStatusCode"]


class Rekognition():
    def __init__(self, profile, region=DEFAULTS["region_name"]):
        self.profile = profile
        self.region_name = region
        self.client = self.get_client()

    def get_client(self):
        session = boto3.Session(profile_name=self.profile)
        client = session.client("rekognition", region_name=self.region_name)
        return client

    def list_collections(self):
        ret = self.client.list_collections()
        if status_code(ret) == 200:
            print("list_collections: {}".format(ret["CollectionIds"]))
            return ret["CollectionIds"]
        print(status_code(ret))
        return []

    def collection_exist(self, collection_id):
        return collection_id in self.list_collections()

    def list_faces(self, collection_id):
        ret = self.client.list_faces(CollectionId=collection_id)
        if status_code(ret) == 200:
            for face in ret["Faces"]:
                print("FaceId: {}".format(face["FaceId"]))
                print("ImageId: {}".format(face["ImageId"]))
                print("ExternalImageId: {}".format(face["ExternalImageId"]))
                print("Confidence: {}".format(face["Confidence"]))
            return ret["Faces"]
        print(status_code(ret))
        return []

    def create_collection(self, collection_id):
        try:
            ret = self.client.create_collection(CollectionId=collection_id)
            print(ret)
            return True
        except Exception as e:
            print(e)
        return False

    def delete_collection(self, collection_id):
        try:
            ret = self.client.delete_collection(CollectionId=collection_id)
            print(ret)
            return True
        except Exception as e:
            print(e)
        return False

    def index_faces(self, image_file, external_image_id, collection_id):
        with open(image_file, "rb") as image:
            ret = self.client.index_faces(
                CollectionId=collection_id,
                Image={"Bytes": image.read()},
                ExternalImageId=external_image_id
            )
            if status_code(ret) == 200:
                for rec in ret["FaceRecords"]:
                    face = rec["Face"]
                    print("FaceId: {}".format(face["FaceId"]))
                    print("ImageId: {}".format(face["ImageId"]))
                    print("ExternalImageId: {}".format(face["ExternalImageId"]))
                    print("Confidence: {}".format(face["Confidence"]))
                return True
            print("Unexpected status code: {}".format(status_code(ret)))
        return False

    def search_faces_by_image(self, image_file, external_image_id, collection_id):
        """
        :param image_file:
        :param external_image_id:
        :param collection_id:
        :return: ExternalImageId if find a match; None if unable to find a match
        """
        id = None
        similarity = 0.0
        with open(image_file, "rb") as image:
            print("Searching faces ...")
            ret = self.client.search_faces_by_image(
                CollectionId=collection_id,
                Image={"Bytes": image.read()},
            )
            print(ret)
            if status_code(ret) == 200:
                for rec in ret["FaceMatches"]:
                    if external_image_id is not None and rec["Face"]["ExternalImageId"] != external_image_id:
                        continue
                    if rec["Similarity"] > similarity:
                        id = rec["Face"]["ExternalImageId"]
                    print("Similarity: {}".format(rec["Similarity"]))
                    print("FaceId: {}".format(rec["Face"]["FaceId"]))
                    print("ImageId: {}".format(rec["Face"]["ImageId"]))
                    print("ExternalImageId: {}".format(rec["Face"]["ExternalImageId"]))
                    print("Confidence: {}".format(rec["Face"]["Confidence"]))
        return id
