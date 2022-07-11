import os
import PIL

os.environ["AWS_PROFILE"] = "d4data"
from object_ai.repos import S3ImagesRepo


def test_s3_repo_returns_image():
    s3 = S3ImagesRepo(
        "object-ai-test-bucket2", base_path="PennFudanPed/PNGImages", region="us-east-2"
    )
    image = s3.get_image("FudanPed00001.png")
    assert type(image) == PIL.PngImagePlugin.PngImageFile


def test_s3_repo_list_images():
    repo = S3ImagesRepo(
        "object-ai-test-bucket2", base_path="PennFudanPed/PNGImages", region="us-east-2"
    )
    expected_images = ["FudanPed00001.png", "FudanPed00002.png", "FudanPed00003.png"]
    images = repo.list_image_names()
    assert expected_images == images
