import xphid
import re
from atproto import Client, models, client_utils
import typing as t

def maybethiswilluploadimages(imagepaths,textpost):
    allimages=[]
    print('running through uploadimages with image paths',imagepaths,'and textpost',textpost)
    for imagepath in imagepaths:
        with open(imagepath, 'rb') as file:
            img_data=file.read()
            print('read file')
            upload=bskyclient.com.atproto.repo.upload_blob(img_data)
            print('uploaded image')
            allimages.append(models.AppBskyEmbedImages.Image(alt='crossposted with xpbsky: no alt text available', image=upload.blob))
            file.close()
            print('uploaded image from',imagepath)
    embed = models.AppBskyEmbedImages.Main(images=allimages)
    bskyclient.com.atproto.repo.create_record(
        models.ComAtprotoRepoCreateRecord.Data(
            repo=bskyclient.me.did,
            collection=models.ids.AppBskyFeedPost,
            record=models.AppBskyFeedPost.Main(
                created_at=bskyclient.get_current_time_iso(), text=textpost, facets=combo_inject(textpost), embed=embed
            ),
        )
    )
    print('posted image tweet')

def combo_positions(text: str, *, encoding: str = 'UTF-8'):
    """This function will detect any links beginning with http or https."""
    #https://github.com/MarshalX/atproto/blob/main/examples/advanced_usage/auto_hyperlinks.py
    encoded_text = text.encode(encoding)

    # Adjusted URL matching pattern
    urlpattern = rb'https?://[^ \n\r\t]*'
    hashpattern= rb'#.\S*'

    urlmatches = re.finditer(urlpattern, encoded_text)
    hashmatches = re.finditer(hashpattern, encoded_text)
    url_byte_positions = []
    hash_byte_positions = []

    for match in urlmatches:
        url_bytes = match.group(0)
        url = url_bytes.decode(encoding)
        url_byte_positions.append((url, match.start(), match.end()))

    for match in hashmatches:
        hash_bytes = match.group(0)
        hash = hash_bytes.decode(encoding)
        hash_byte_positions.append((hash, match.start(), match.end()))

    return (url_byte_positions,hash_byte_positions)

def combo_inject(text: str):

    url_positions, hash_positions = combo_positions(text)
    facets = []

    for link_data in url_positions:
        uri, byte_start, byte_end = link_data
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Link(uri=uri)],
                index=models.AppBskyRichtextFacet.ByteSlice(byte_start=byte_start, byte_end=byte_end),
            )
        )

    for link_data in hash_positions:
        hash, byte_start, byte_end = link_data
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Tag(tag=hash[1:])],
                index=models.AppBskyRichtextFacet.ByteSlice(byte_start=byte_start, byte_end=byte_end),
            )
        )
    
    return facets


# def extract_url_byte_positions(text: str, *, encoding: str = 'UTF-8') -> t.List[t.Tuple[str, int, int]]:
#     """This function will detect any links beginning with http or https."""
#     #https://github.com/MarshalX/atproto/blob/main/examples/advanced_usage/auto_hyperlinks.py
#     encoded_text = text.encode(encoding)

#     # Adjusted URL matching pattern
#     pattern = rb'https?://[^ \n\r\t]*'

#     matches = re.finditer(pattern, encoded_text)
#     url_byte_positions = []

#     for match in matches:
#         url_bytes = match.group(0)
#         url = url_bytes.decode(encoding)
#         url_byte_positions.append((url, match.start(), match.end()))

#     return url_byte_positions

# def injecturls(text: str):

#     url_positions = extract_url_byte_positions(text)
#     facets = []

#     for link_data in url_positions:
#         uri, byte_start, byte_end = link_data
#         facets.append(
#             models.AppBskyRichtextFacet.Main(
#                 features=[models.AppBskyRichtextFacet.Link(uri=uri)],
#                 index=models.AppBskyRichtextFacet.ByteSlice(byte_start=byte_start, byte_end=byte_end),
#             )
#         )
#     return facets

def sendtweet(text,images):
    maybethiswilluploadimages(images,text)
    print('bsky sent')


bskyclient=Client()
bskyclient.login('tetracado.bsky.social', xphid.bskyapppass)
print('logged in to bsky')

